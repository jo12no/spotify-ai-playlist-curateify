# Spotify AI Playlist: Curateify 🎧🤖

TL:DR - End to end automated to Spotify, prompt a LLM for a custom playlist (eg. `"for fans of tame impala on a rainy morning:`) from your terminal. Alternatively, can use a `.txt` file with format `artist - track` and automatically make a playlist. 

An experimental CLI application designed to automate the curation of Spotify playlists via inference with multiple AI models. It supports multiple data sources including:
1) GPT & Gemini model outputs
2) Spotify API (`get-recommendations` endpoint).
3) Local .txt file (list of tracks or artist names exported from any service). 

## Features

- **Personalised Suggestions**: tuned towards "less mainstream" and "less popular" choices to enhance the discoverability of lesser-known artists who are typically overlooked by standard recommendations on the platform, but still receptive to user prompts. 
- **Playlist Management**: Create new playlists or update existing ones using Spotify's API.
- **User Interactions**: Simple prompts guide users through track selection and playlist configuration.
- **Advanced Processing**: Choose to process tracks individually or by artist for tailored playlist curation.


## Usage

To run the application, simply run it from your command line:

`python main.py`

You can customize `config.py` for settings. 

## Example flow
<img width="793" alt="example" src="https://github.com/jo12no/spotify-ai-playlist-curateify/assets/19522573/1b204a18-2461-4ec3-a541-4c599a153b10">


## Installation

Before running the script, you need to ensure you have Python installed on your system and the necessary Python package:

```
pip install -r requirements.txt
```

## Dependencies

- Python 3.x
- `spotipy`
- `google-cloud-aiplatform`
- `openai`
- `gcloud-sdk`

## Considerations/Acknowledgments

- Thanks to Spotify for providing a great API and the `spotipy` library! 
