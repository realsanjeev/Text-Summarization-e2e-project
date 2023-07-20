import os
import sys

from src.configuration.config import DataValidationConfig
from src.logger import logging
from src.exception import CustomException

class DataValidation:
    def __init__(self, config: DataValidationConfig) -> None:
        self.config = config

    def validate_files(self):
        try:
            validation_status = False
            all_files = os.listdir(os.path.join("artifacts", "data_ingestion", "samsum_dataset"))
            for file in all_files:
                if file not in self.config.ALL_REQUIRED_FILES:
                    validation_status = False
                else:
                    validation_status = True
                with open(self.config.STATUS_FILE, 'a', encoding='utf-8') as file_fp:
                    file_fp.write(f"Validation status of {file}: {validation_status}")
                logging.info(f"{file} Files validation Success. \
                    VALIDATION_STATUS: {validation_status}")
            return validation_status

        except Exception as err:
            logging.warning(f"Cannot validate due to error: \n{err}")
            raise CustomException(err, sys) from err
