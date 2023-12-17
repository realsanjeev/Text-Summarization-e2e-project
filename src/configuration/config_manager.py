import os
from pathlib import Path

from src.constants import CONFIG_FILE_PATH, PARAMS_FILE_PATH
from src.logger import logging
from src.utils import read_yaml
from src.configuration.config import (
    DataIngestionConfig,
    DataTransformationConfig,
    DataValidationConfig,
    ModelTrainerConfig,
    ModelEvaluationConfig,
)

class ConfigurationManager:
    def __init__(self, config_file_path=Path(CONFIG_FILE_PATH),
    param_file_path=Path(PARAMS_FILE_PATH)) -> None:
        self.config = read_yaml(config_file_path)
        self.params = read_yaml(param_file_path)

        os.makedirs(self.config.artifacts_root, exist_ok=True)
    
    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion
        os.makedirs(config.root_dir, exist_ok=True)

        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            source_URL=config.source_URL,
            local_data_path=config.local_data_path,
            unzip_dir=config.unzip_dir
        )
        return data_ingestion_config
    
    def get_data_validation_config(self) -> DataValidationConfig:
        config = self.config.data_validation
        os.makedirs(config.root_dir, exist_ok=True)

        data_validation_config = DataValidationConfig(
            root_dir=config.root_dir,
            STATUS_FILE=config.STATUS_FILE,
            ALL_REQUIRED_FILES=config.ALL_REQUIRED_FILES 
        )
        return data_validation_config
    
    def get_data_transformation_config(self) -> DataTransformationConfig:
        config = self.config.data_transformation
        os.makedirs(config.root_dir, exist_ok=True)

        data_transformation_config = DataTransformationConfig(
            root_dir=config.root_dir,
            data_path=config.data_path,
            tokenizer_name=config.tokenizer_name
        )
        return data_transformation_config
 
    def get_model_trainer_config(self) -> ModelTrainerConfig:
        config = self.config.model_trainer
        params = self.params.TrainingArguments
        os.makedirs(config.root_dir, exist_ok=True)

        model_trainer_config = ModelTrainerConfig(
            root_dir=config.root_dir,
            data_path=config.data_path,
            model_ckpt = config.model_ckpt,
            num_train_epochs = params.num_train_epochs,
            warmup_steps = params.warmup_steps,
            per_device_train_batch_size = params.per_device_train_batch_size,
            weight_decay = params.weight_decay,
            logging_steps = params.logging_steps,
            evaluation_strategy = params.evaluation_strategy,
            eval_steps = params.eval_steps,
            save_steps = params.save_steps,
            gradient_accumulation_steps = params.gradient_accumulation_steps
        )
        return model_trainer_config
    
    def get_model_evaluation_config(self) -> ModelEvaluationConfig:
        config = self.config.model_evaluation
        os.makedirs(config.root_dir, exist_ok=True)

        model_evaluation_config = ModelEvaluationConfig(
            root_dir=config.root_dir,
            data_path=config.data_path,
            model_path = config.model_path,
            tokenizer_path = config.tokenizer_path,
            metric_file_name = config.metric_file_name
        )
        return model_evaluation_config
