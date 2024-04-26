import os
import time

import config
import spotipy
from spotipy.oauth2 import SpotifyOAuth


class SpotifyService:
    """
    Provides a service layer for interacting with the Spotify API.

    This class handles authentication and provides methods to interact with
    the Spotify API, such as creating playlists, searching for tracks,
    adding tracks to playlists, and fetching user playlist information.
    """
    def __init__(self):
        """
        Initializes the SpotifyService with necessary credentials and scopes.
        
        The client ID, client secret, and scopes are retrieved from environment variables
        or a configuration object. An authenticated spotipy.Spotify client is created.
        """
        self.SPOTIPY_CLIENT_ID = os.getenv(
            "SPOTIFY_CLIENT_ID", config.SpotifyConfig.SPOTIFY_CLIENT_ID
        )
        self.SPOTIPY_CLIENT_SECRET = os.getenv(
            "SPOTIFY_CLIENT_SECRET", config.SpotifyConfig.SPOTIFY_CLIENT_SECRET
        )
        self.SPOTIPY_REDIRECT_URI = "http://localhost/"
        self.SPOTIPY_SCOPE = config.SpotifyConfig.SPOTIPY_SCOPE
        self.sp = self.spotipy_client()

    def spotipy_client(self):
        """
        Creates an authenticated Spotify client using OAuth.

        Returns:
            spotipy.Spotify: An authenticated spotipy.Spotify client instance.
        """
        sp = spotipy.Spotify(  # retries=0,
            auth_manager=SpotifyOAuth(
                scope=self.SPOTIPY_SCOPE,
                client_id=self.SPOTIPY_CLIENT_ID,
                client_secret=self.SPOTIPY_CLIENT_SECRET,
                redirect_uri=self.SPOTIPY_REDIRECT_URI,
            )
        )
        return sp

    def get_current_user_id(self):
        """
        Retrieves the current authenticated user's Spotify ID.
        Used as a required parameter when creating a new playlist.

        Returns:
            str: The Spotify user ID of the current authenticated user.
        """
        return self.sp.current_user()["id"]

    def create_playlist_and_return_id(self):
        """
        Creates a new public Spotify playlist for the current user and returns its ID.

        The name of the playlist is obtained through user input.

        Returns:
            str: The Spotify playlist ID of the newly created playlist.
        """
        current_username = self.get_current_user_id()
        playlist_name = input("enter playlist name > ")
        playlist = self.sp.user_playlist_create(
            user=current_username, name=playlist_name, public=True, collaborative=False
        )
        print(f"Playlist '{playlist_name}' created with ID: {playlist['id']}")
        return playlist["id"]

    def fetch_track_id_from_search(self, query, limit=1):
        """
        Searches Spotify for tracks based on a query string and returns the search results.
        Fetches an array of search results - we only want index 0.

        Parameters:
            query (str): The search query string.
            limit (int): The number of search results to return (default is 1).

        Returns:
            dict or None: The search result containing track information or None if an error occurs.
        """
        try:
            result = self.sp.search(q=query, type="track", limit=limit)
        except Exception as e:
            print(f"error searching for {query}... pausing for a few moments")
            time.sleep(4)
            return None
        return result

    def process_tracks(self, list_of_tracks_to_process):
        """
        Processes a list of track names by searching for them and retrieving their Spotify IDs.
        Calls the fetch_track_id_from_search method for each track to get the ID.

        Parameters:
            list_of_tracks_to_process (list of str): A list of track names to be processed.

        Returns:
            list of str: A list of Spotify track IDs corresponding to the searched tracks.
        """
        print("Processing by individual track.")
        list_of_track_ids_to_add = []
        for idx, track in enumerate(list_of_tracks_to_process):
            # could improve the query potentially by using.. artist:"X" track:"Y"
            try:
                result = self.fetch_track_id_from_search(track)
                sp_track_id = result["tracks"]["items"][0]["id"]
                list_of_track_ids_to_add.append(sp_track_id)

                print(
                    f"#{idx+1} of {len(list_of_tracks_to_process)}. searched for: {track}"
                )
                print(
                    f"returned: {result['tracks']['items'][0]['artists'][0]['name']} - {result['tracks']['items'][0]['name']}"
                )
                time.sleep(3)
            except Exception as e:
                print(f"Skipping track due to a fatal error: {e}")

        return list_of_track_ids_to_add

    def process_tracks_by_artist(self, list_of_tracks_to_process, limit=5):
        """
        Processes a list of artist names by searching for their tracks and retrieving up to a limit of Spotify IDs.
        5 tracks for each by default. 

        Parameters:
            list_of_tracks_to_process (list of str): A list of artist names to be processed.
            limit (int): The maximum number of track IDs to return per artist (default is 5).

        Returns:
            list of str: A list of Spotify track IDs corresponding to the searched artists' tracks.
        """
        print(f"Processing by artist - returning {limit} tracks for each search.")
        list_of_track_ids_to_add = []
        for idx, artist in enumerate(list_of_tracks_to_process):
            try:
                query = f"artist:{artist}"
                result = self.fetch_track_id_from_search(query, limit=limit)
                for x in result["tracks"]["items"]:
                    sp_track_id = x["id"]
                    list_of_track_ids_to_add.append(sp_track_id)
                    print(f"returned: {x['artists'][0]['name']} - {x['name']}")

                print(
                    f"#{idx+1} of {len(list_of_tracks_to_process)}. {len(list_of_tracks_to_process) - idx} remain. searched for: {artist}"
                )

                time.sleep(3)
            except Exception as e:
                print(f"Skipping artist due to a fatal error: {e}")

        return list_of_track_ids_to_add

    def add_track_ids_to_playlist(self, list_of_track_ids_to_add, playlist_id):
        """
        Adds a list of track IDs to a given Spotify playlist in batches of up to 100 items.

        Parameters:
            list_of_track_ids_to_add (list of str): A list of Spotify track IDs to be added to the playlist.
            playlist_id (str): The Spotify playlist ID where tracks will be added.

        Returns:
            None
        """
        track_id_count = len(list_of_track_ids_to_add)
        print(f"Attempting to add batches of {track_id_count} track ids into playlist")
        for track_id_idx in range(0, track_id_count, 100):
            self.sp.playlist_add_items(
                playlist_id, list_of_track_ids_to_add[track_id_idx : track_id_idx + 100]
            )
            time.sleep(1.5)
        print("Completed adding tracks to playlist!")

    def fetch_user_playlists(self):
        """
        Fetches all playlists created by the current user and returns their names and Spotify URLs.

        Returns:
            list of [str, str]: A list containing pairs of playlist names and their corresponding Spotify URLs.
        """
        playlist_name_store = []

        results = self.sp.current_user_playlists()
        while results:
            for result in results["items"]:
                playlist_name_store.append(
                    [result["name"], result["external_urls"]["spotify"]]
                )
            if results["next"]:
                results = self.sp.next(results)
            else:
                break

        return playlist_name_store
