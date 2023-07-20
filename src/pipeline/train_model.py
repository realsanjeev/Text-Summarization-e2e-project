import sys

from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.data_validation import DataValidation
from src.pipeline.model_evaluator import ModelEvaluation
from src.pipeline.model_trainer import ModelTrainer

from src.configuration.config_manager import ConfigurationManager
from src.exception import CustomException

try:
    config = ConfigurationManager()
    data_ingestion_config = config.get_data_ingestion_config()
    data_ingestion_config = config.get_data_ingestion_config()
    data_ingestion = DataIngestion(config=data_ingestion_config)
    data_ingestion.download_dataset()
    data_ingestion.extract_zip_file()

    data_validation_config = config.get_data_validation_config()
    data_validation = DataValidation(config=data_validation_config)
    data_validation.validate_files()

    data_transformation_config = config.get_data_transformation_config()
    data_transformation = DataTransformation(config=data_transformation_config)
    data_transformation.convert()
    tokenizer = data_transformation.get_tokenizer()

    model_trainer_config = config.get_model_trainer_config()
    model_trainer_config = ModelTrainer(config=model_trainer_config)
    model_trainer_config.train(tokenizer=tokenizer)

    model_evaluation_config = config.get_model_evaluation_config()
    model_evaluation_config = ModelEvaluation(config=model_evaluation_config)
    # model_evaluation_config.evaluate()
except Exception as err:
    raise CustomException(err, sys) from err
