from vertexai.preview.generative_models import GenerativeModel  # enterprise
import config


class GeminiFetcher:
    """
    Fetches responses from the Gemini model using the Vertex AI platform.

    This class encapsulates the functionality to interact with the Gemini Pro model,
    providing an interface to send prompts and receive generated content.
    """
    def __init__(self):
        """
        Initializes a new instance of the GeminiFetcher class, setting up
        the client to interact with the Gemini model using credentials
        and configurations specified in the `config` module, defaulting to gCloud SDK.
        """
        MODEL_NAME = config.GeminiConfig.MODEL_NAME
        MODEL_PARAMS = config.GeminiConfig.MODEL_PARAMS

        self.gemini_client = GenerativeModel(
            model_name=MODEL_NAME, generation_config=MODEL_PARAMS
        )

    def fetch_gemini_response(self):
        """
        Sends a prompt to the Gemini model and retrieves the generated response.

        The method constructs a payload for the model based on predefined session
        prompts and user input. It then sends this payload to the model and returns
        the generated text as a response.

        Returns:
            str: The text generated by the Gemini model in response to the input prompt.
        """
        prompt_payload = [
            f"{config.GeminiConfig.SESSION_PROMPT}",
            f"input: {input('prompt > ')}",
            "output: ",
        ]

        response = self.gemini_client.generate_content(prompt_payload)
        return response.text
