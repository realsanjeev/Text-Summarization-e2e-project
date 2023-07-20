import time
import os
import torch

from transformers import TrainingArguments, Trainer
from transformers import DataCollatorForSeq2Seq
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from datasets import load_from_disk

from src.configuration.config import ModelTrainerConfig
from src.logger import logging
from src.exception import CustomException

class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config

    def train(self, tokenizer=None):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        logging.info(f">>>>>>>> Model trainer initiated using '{device.upper()}' <<<<<<<<<<<")
        prev_time = time.time()

        if tokenizer is None:
            tokenizer = AutoTokenizer.from_pretrained(self.config.model_ckpt)
        model_pegasus = AutoModelForSeq2SeqLM.from_pretrained(self.config.model_ckpt).to(device)
        seq2seq_data_collator = DataCollatorForSeq2Seq(tokenizer, model=model_pegasus)
        
        logging.info(f"Downloading the pretrained model '{self.config.model_ckpt}'")
        #loading data 
        dataset_samsum_pt = load_from_disk(self.config.data_path)

        trainer_args = TrainingArguments(
            output_dir=self.config.root_dir,
            num_train_epochs=self.config.num_train_epochs,
            warmup_steps=self.config.warmup_steps,
            per_device_train_batch_size=self.config.per_device_train_batch_size,
            per_device_eval_batch_size=self.config.per_device_train_batch_size,
            weight_decay=self.config.weight_decay,
            logging_steps=self.config.logging_steps,
            evaluation_strategy=self.config.evaluation_strategy,
            eval_steps=self.config.eval_steps,
            save_steps=1e6,
            gradient_accumulation_steps=self.config.gradient_accumulation_steps
        )

        trainer = Trainer(model=model_pegasus,
                          args=trainer_args,
                          tokenizer=tokenizer,
                          data_collator=seq2seq_data_collator,
                          train_dataset=dataset_samsum_pt["train"],
                          eval_dataset=dataset_samsum_pt["validation"])
        logging.info("Model training started......")
        trainer.train()
        current_time = time.time()

        logging.info(f"Model trained Successfully in {current_time-prev_time:%.2f} sec")

        ## Save model
        model_save_path = os.path.join(self.config.root_dir, "pegasus-samsum-model")
        model_pegasus.save_pretrained(model_save_path)
        ## Save tokenizer
        tokenizer_save_path = os.path.join(self.config.root_dir, "tokenizer")
        tokenizer.save_pretrained(tokenizer_save_path)

