import os
from openai import OpenAI
import config

class GptFetcher:
    """
    GptFetcher is a class responsible for interacting with the OpenAI API to fetch responses from the GPT model.

    Attributes:
        API_KEY (str): The API key used to authenticate requests to the OpenAI API.
        SESSION_PROMPT (str): The initial prompt that sets the context for the conversation with the GPT model.
        MODEL_PARAMS (dict): Parameters for the GPT model configuration.
        gpt_client (OpenAI): An instance of the OpenAI client.

    Methods:
        create_client(): Creates an OpenAI client using the API key.
        fetch_gpt_response(): Fetches a response from the GPT model based on user input.
    """
    def __init__(self):
        """
        Initializes the GptFetcher instance, setting up the API key, session prompt, model parameters, and creating the GPT client.
        """
        self.API_KEY = config.OpenAIConfig.API_KEY if config.OpenAIConfig.API_KEY else os.getenv("OPENAI_API_KEY")
        self.SESSION_PROMPT = config.OpenAIConfig.SESSION_PROMPT
        self.MODEL_PARAMS = config.OpenAIConfig.MODEL_PARAMS
        self.gpt_client = self.create_client()

    def create_client(self):
        """
        Creates an OpenAI client with the specified API key. Raises an error if the API key is not provided.

        Returns:
            OpenAI: A client object for interacting with the OpenAI API.

        Raises:
            ValueError: If the API key is not set in the config file or environment variable.
        """
        if not self.API_KEY:
            raise ValueError("API key must be set in config file or environment variable.")
        gpt_client = OpenAI(api_key=self.API_KEY)
        return gpt_client
    
    def fetch_gpt_response(self):
        """
        Fetches a response from the GPT model based on user input.

        The method prompts the user for input, sends it to the GPT model, and returns the model's response.

        Returns:
            str: The content of the message from the GPT model's response.
        """
        completion = self.gpt_client.chat.completions.create(
        **self.MODEL_PARAMS,
        messages=[
            {"role": "system", "content": self.SESSION_PROMPT},
            {"role": "user", "content": input('enter prompt > ')}
        ]
        )

        response = completion.choices[0].message.content
        return response
