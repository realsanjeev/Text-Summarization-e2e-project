import torch
import time
import os
import pandas as pd

from transformers import TrainingArguments, Trainer
from transformers import DataCollatorForSeq2Seq
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from datasets import load_from_disk

from src.configuration.config import ModelEvaluationConfig
from src.logger import logging
from src.exception import CustomException

class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config
        
    def generate_batch_sized_chunks(list_of_elements, batch_size: int):
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

    def evaluate(self, device=None):
        if device not in ["cpu", "cuda"]:
            device = "cuda" if torch.cuda.is_available() else "cpu"
        tokenizer = AutoTokenizer.from_pretrained(self.config.tokenizer_path, use_fast=False)
        model_pegasus = AutoModelForSeq2SeqLM.from_pretrained(self.config.model_path).to(device)
       
        #loading data 
        dataset_samsum_pt = load_from_disk(self.config.data_path)
        rouge_names = ["rouge1", "rouge2", "rougeL", "rougeLsum"]
  
        # rouge_metric = load_metric('rouge')

        # score = self.calculate_metric_on_test_ds(
        # dataset_samsum_pt['test'][0:10], rouge_metric, model_pegasus, tokenizer, batch_size = 2, column_text = 'dialogue', column_summary='summary'
        #     )

        # rouge_dict = dict((rn, score[rn].mid.fmeasure ) for rn in rouge_names )
        rouge_dict={}
        df = pd.DataFrame(rouge_dict, index=['pegasus'] )
        df.to_csv(self.config.metric_file_name, index=False)
        