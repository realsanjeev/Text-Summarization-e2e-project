import sys
import torch
import pandas as pd
import evaluate

from tqdm.auto import tqdm
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from datasets import load_from_disk

from src.configuration.config import ModelEvaluationConfig
from src.logger import logging
from src.exception import CustomException

class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config

    def generate_batch_sized_chunks(self, list_of_elements, batch_size: int):
        '''
        Generate batch-sized chunks from a given list of elements.

        Args:
            list_of_elements (List): The input list of elements.
            batch_size (int): The desired batch size for chunking.

        Yields:
            List: A batch-sized chunk of elements from the input list.

        Example:
            >>> elements = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            >>> batch_size = 3
            >>> for batch in generate_batch_sized_chunks(elements, batch_size):
            >>>     print(batch)
            [1, 2, 3]
            [4, 5, 6]
            [7, 8, 9]
        '''
        for index in range(0, len(list_of_elements), batch_size):
            yield list_of_elements[index: index + batch_size]

    def calculate_metric(self, dataset,
                        metric, model, tokenizer,
                        device, batch_size=16,
                        column_text='articles', column_summary='highlights'):
        try:
            article_batches = list(self.generate_batch_sized_chunks(
                dataset[column_text], batch_size)
                )
            target_batches= list(self.generate_batch_sized_chunks(
                dataset[column_summary], batch_size)
                )

            for article_batch, target_batch in tqdm(zip(article_batches, target_batches)):

                inputs = tokenizer(article_batch, max_length=1024,  truncation=True,
                                padding="max_length", return_tensors="pt")

                summaries = model.generate(input_ids=inputs["input_ids"].to(device),
                                            attention_mask=inputs["attention_mask"].to(device),
                                            length_penalty=0.8,
                                            num_beams=8,
                                            max_length=128)

                # Finally, we decode the generated texts,
                # replace the  token, and add the decoded texts with the references to the metric.
                decoded_summaries = [tokenizer.decode(summary, skip_special_tokens=True,
                                                    clean_up_tokenization_spaces=True)
                                    for summary in summaries]

                decoded_summaries = [summary.replace("", " ") for summary in decoded_summaries]

                metric.add_batch(predictions=decoded_summaries, references=target_batch)

            #  Finally compute and return the ROUGE scores.
            score = metric.compute()
            return score
        except Exception as err:
            raise CustomException(err, sys) from err

    def evaluate(self, device=None):
        logging.info('Model evaluation initiated')
        if device not in ["cpu", "cuda"] or device=='cuda':
            device = "cuda" if torch.cuda.is_available() else "cpu"
        tokenizer = AutoTokenizer.from_pretrained(self.config.tokenizer_path, use_fast=False, clean_up_tokenization_spaces=True)
        model_pegasus = AutoModelForSeq2SeqLM.from_pretrained(self.config.model_path).to(device)

        #loading data
        dataset_loader = load_from_disk(self.config.data_path)
        rouge_names = ["rouge1", "rouge2", "rougeL", "rougeLsum"]

        rouge_metric = evaluate.load('rouge')

        score = self.calculate_metric(
        dataset=dataset_loader['test'][0:10], metric=rouge_metric,
        model=model_pegasus, tokenizer=tokenizer,
        batch_size=2, device=device,
        column_text='dialogue', column_summary='summary'
            )

        rouge_dict = dict((rn, score[rn].mid.fmeasure ) for rn in rouge_names )
        metric_df = pd.DataFrame(rouge_dict, index=['pegasus'] )
        metric_df.to_csv(self.config.metric_file_name, index=False)
        return metric_df
