import os
from src.configuration.config import DataTransformationConfig
from src.logger import logging
from src.exception import CustomException

from transformers import AutoTokenizer
from datasets import load_from_disk

class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config
        self.tokenizer = AutoTokenizer.from_pretrained(config.tokenizer_name, use_fast=False)
    
    def convert_to_features(self, batch_data):
        # Tokenize the dialogue in the batch using the tokenizer
        input_encodings = self.tokenizer(batch_data['dialogue'], max_length=1024, truncation=True)

        # Tokenize the summary in the batch using the tokenizer as the target tokenizer
        with self.tokenizer.as_target_tokenizer():
            target_encodings = self.tokenizer(batch_data['summary'], max_length=128, truncation=True)

        # Return the converted features as a dictionary
        return {
            'input_ids': input_encodings['input_ids'],         # Input token IDs
            'attention_mask': input_encodings['attention_mask'],  # Attention mask
            'labels': target_encodings['input_ids']             # Target token IDs for the model's training
        }
    
    def get_tokenizer(self):
        return self.tokenizer
    
    def convert(self):
        dataset_samsum = load_from_disk(self.config.data_path)
        dataset_samsum_pt = dataset_samsum.map(self.convert_to_features, batched=True)
        dataset_samsum_pt.save_to_disk(os.path.join(self.config.root_dir,"samsum_dataset"))
        logging.info("Converting dataset in batch")