import os
import sys
import zipfile
from urllib import request
from pathlib import Path

from src.configuration.config import DataIngestionConfig
from src.logger import logging
from src.utils import get_size
from src.exception import CustomException

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def download_dataset(self):
        '''Download dataset if not exists loacal disk'''
        if not os.path.exists(self.config.local_data_path):
            file, header = request.urlretrieve(url=self.config.source_URL,
                                               filename=self.config.local_data_path)
            logging.info(f"{file} successfully downloaded! Info: \n{header}")
        else:
            logging.info(f"File already exists of size:\
                         {get_size(Path(self.config.local_data_path))} KB")

    def extract_zip_file(self, unzip_path=None):
        """Extract zip file to specified path

        Args:
            unzip_path: str, optional
                The path to extract the zip file to. If not provided,\
                    it defaults to `self.config.unzip_dir`.
        """
        if unzip_path is None:
            unzip_path = self.config.unzip_dir
        try:
            os.makedirs(unzip_path, exist_ok=True)
            with zipfile.ZipFile(self.config.local_data_path, 'r') as zip_fp:
                zip_fp.extractall(unzip_path)
                logging.info("Dataset successfully extracted.")
        except Exception as err:
            logging.warning(f"Error while extracting file path: {unzip_path}")
            logging.error(f"Error explaination: {err}")
            raise CustomException(err, sys) from err
