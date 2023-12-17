import sys
from transformers import AutoTokenizer
from transformers import pipeline

from src.configuration.config_manager import ConfigurationManager
from src.exception import CustomException

class PredictionPipeline:
    def __init__(self):
        '''
        Initialize the PredictionPipeline class for generating model predictions.

        The constructor retrieves the model evaluation configuration\
            using the ConfigurationManager and loads the tokenizer
        from the specified tokenizer_path.

        Raises:
            CustomException: If any error occurs while initializing the tokenizer,\
                it will be captured and raised as a CustomException.
        '''
        self.config = ConfigurationManager().get_model_evaluation_config()
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.config.tokenizer_path)
        except Exception as err:
            raise CustomException(err, sys) from err

    def predict(self, text: str, max_length: int=64, num_beams: int=8) -> str:
        '''
        Generate a summary prediction for the given input text.

        Args:
            text (str): The input text for which the summary needs to be generated.
            max_length (int, optional): The maximum length of the summary. Default is 64.
            num_beams (int, optional): The number of beams for beam search. Default is 8.

        Returns:
            str: The generated summary text.

        Example:
            >>> pipeline = PredictionPipeline()
            >>> input_text = "This is a long piece of text that needs to be summarized."
            >>> summary = pipeline.predict(input_text, max_length=100, num_beams=4)
            >>> print(summary)
            "This is a summary of the long piece of text."
        '''
        gen_kwargs = {"length_penalty": 0.8, "num_beams": num_beams, "max_length": max_length}
        pipe = pipeline("summarization", model=self.config.model_path, tokenizer=self.tokenizer)

        output = pipe(text, **gen_kwargs)[0]["summary_text"]
        print("\nModel Summary:")
        print(output)
        return output
