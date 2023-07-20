import os
import sys

from transformers import AutoTokenizer
from datasets import load_from_disk

from src.configuration.config import DataTransformationConfig
from src.logger import logging
from src.exception import CustomException

class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config
        self.tokenizer = AutoTokenizer.from_pretrained(config.tokenizer_name, use_fast=False)

    def convert_to_features(self, batch_data, tokenizer=None):
        try:
            if tokenizer is None:
                tokenizer = self.tokenizer
            # Tokenize the dialogue in the batch using the tokenizer
            input_encodings = tokenizer(batch_data['dialogue'], max_length=1024, truncation=True)

            # Tokenize the summary in the batch using the tokenizer as the target tokenizer
            target_encodings = tokenizer(batch_data['summary'],
                                         max_length=128, truncation=True,
                                         text_target=batch_data['summary'])
        except Exception as err:
            raise CustomException(err, sys) from err

        # Return the converted features as a dictionary
        return {
            'input_ids': input_encodings['input_ids'],         # Input token IDs
            'attention_mask': input_encodings['attention_mask'],  # Attention mask
            'labels': target_encodings['input_ids']  # Target token IDs for the model's training
        }

    def get_tokenizer(self):
        return self.tokenizer

    def convert(self):
        try:
            dataset = load_from_disk(self.config.data_path)
            dataset_batch_path = os.path.join(self.config.root_dir, "samsum_dataset")
            if os.path.exists(dataset_batch_path):
                logging.warning(f"Batched dataset alreay exist at path: {dataset_batch_path}")
                return dataset_batch_path
            dataset_in_batch = dataset.map(self.convert_to_features, batched=True)
            dataset_in_batch.save_to_disk(dataset_batch_path)
            logging.info(f"Converting dataset in batch sucessful \
                         and saved at: {dataset_batch_path}")
        except Exception as err:
            raise CustomException(err, sys) from err
        return dataset_batch_path
