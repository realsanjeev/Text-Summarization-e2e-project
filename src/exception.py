import sys
from src.logger import logging

def error_message_details(error, error_details: sys):

    _, _, exec_obj = error_details.exc_info()
    python_file_name = exec_obj.tb_frame.f_code.co_filename

    error_message = f"[ERROR]: Error occured in python script name\
        [[ '{python_file_name}' ]] line_number [ {exec_obj.tb_lineno} ] error message: [{error}]"
    return error_message

class CustomException(Exception):
    def __init__(self, error, error_detail: sys):
        super().__init__(error)
        self.error = error
        self.error_details = error_detail
        self.error_message = error_message_details(self.error, self.error_details)

    def __str__(self):
        return self.error_message
    
if __name__ == "__main__":
    logging.info("Exception.py is executed")
    try:
        a = 1 / 0
    except Exception as err:
        raise CustomException(err, sys)