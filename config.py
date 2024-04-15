"""Configuration for spotify-ai-playlist-curateify. 

If you have an API key, you can enter it directly here.
However, for better security practices, it is recommended to set it as an 
environment variable.

To use an environment variable, set the API_KEY environment variable in your 
operating system.
If you're unsure how to do this, refer to the documentation specific to your 
operating system or deployment environment.

If you prefer to enter the API key directly (not recommended for production), replace 
'API_KEY' with your actual API key (and Spotify credentials.)

Otherwise, the code will attempt to read the key from the environment variable.
"""


class Constants:
    """
    Constants used for spotify-ai-playlist-curateify.

    Attributes:
        SESSION_PROMPT (str): Instructions provided to the model for supplying music 
                              recommendations.
                              The model is expected to provide a list of tracks in the 
                              format "Artist - Track" without numbering and avoiding 
                              duplicates. The focus should be on less popular
                              tracks to curate a unique playlist.
                              Enable this for an initial prompt, eg: 
                              'You are creative and helpful'.
    """
    SESSION_PROMPT = """
                    You will be asked to supply some music recommendations.
                    You must respond ONLY with a list in the format "Arist - Track". 
                    Don't include the list number (so don't start with 1. etc).
                    List the items without using dashes at the beginning - use plain text.
                    Aim for at least 125 tracks but you can provide as many as you want. 
                    Do not provide duplicates. 
                    Please provide less popular (less mainstream) tracks as much as possible!
                """


class SpotifyConfig:
    """
    Configuration settings specific to the Spotify API.

    Attributes:
        SPOTIPY_SCOPE (str): The scope of access required from Spotify to perform 
                             playlist and library actions (write).
        SPOTIFY_CLIENT_ID (str): The Client ID provided by Spotify when you register 
                             your application. This should be kept secret.
        SPOTIFY_CLIENT_SECRET (str): The Client Secret provided by Spotify upon 
                             application registration. 
                             This should also be kept confidential.
    """
    SPOTIPY_SCOPE = "playlist-modify-public playlist-modify-private user-library-read"
    SPOTIFY_CLIENT_ID = ""
    SPOTIFY_CLIENT_SECRET = ""


class OpenAIConfig:
    """
    Configuration settings for OpenAI's GPT model.

    Attributes:
        API_KEY (str): The API key for authenticating requests to OpenAI's API.
                       It is recommended to set this as an environment variable for 
                       security purposes.
        MODEL_PARAMS (dict): Parameters for configuring the GPT model, including model 
                             name, number of samples, temperature, and max tokens.
        SESSION_PROMPT (str): A prompt inherited from Constants that provides 
                              instructions for generating music recommendations using 
                              OpenAI's model.
    """
    API_KEY = ""

    # Constants
    MODEL_PARAMS = {
        "model": "gpt-4-turbo-2024-04-09",
        "n": 1,  # of samples
        "temperature": 1.0,
        "max_tokens": 500,
    }

    SESSION_PROMPT = Constants.SESSION_PROMPT


class GeminiConfig:
    """
    Configuration settings for the Gemini model.

    Attributes:
        MODEL_NAME (str): Name of the Gemini model to be used.
        MODEL_PARAMS (dict): Parameters for configuring the Gemini model, including 
                             temperature, top_p, top_k, and max_output_tokens.
        SESSION_PROMPT (str): A prompt inherited from Constants that provides 
                             instructions for generating music recommendations using 
                             the Gemini model.
    """
    MODEL_NAME = "gemini-1.0-pro"

    MODEL_PARAMS = {
        "temperature": 0.9,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
    }

    SESSION_PROMPT = Constants.SESSION_PROMPT
