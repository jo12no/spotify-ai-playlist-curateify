class SpotifyFetcher:
    """
    Fetches responses from the Spotify API.

    This class provides methods to interact with the Spotify recommendations endpoint,
    allowing users to retrieve recommended tracks based on seed artists and various
    parameters such as popularity.
    """

    @staticmethod
    def fetch_spotify_response(sp, seed, limit=100):
        """
        Retrieves track recommendations from Spotify based on seed artists and target popularity.

        The method queries the Spotify recommendations API endpoint with the given seed artists
        and optional popularity filter. It allows interactive adjustment of the target popularity
        during runtime and returns a list of track IDs.

        Parameters:
            sp (Spotify): An authenticated spotipy.Spotify client instance.
            seed (list of str): A list of artist IDs to be used as seed for recommendations.
                                 The list is limited to a maximum of 5 artist IDs.
            limit (int): The number of track recommendations to retrieve. Maximum value is 100.

        Returns:
            list of str: A list of Spotify track IDs representing the recommended tracks.

        See Also:
            Spotify Web API Reference for Recommendations:
            https://developer.spotify.com/documentation/web-api/reference/#endpoint-get-recommendations
        """
        target_popularity = 35 # update this as needed -- add to config if often.
        result = sp.sp.recommendations(
            seed_artists=seed, limit=limit, target_popularity=target_popularity
        )

        while True:
            track_ids = SpotifyFetcher().print_and_process_response(result)
            optimise = input(
                f'\nChange "target_popularity" value from {target_popularity} to [0-100]? Otherwise, enter to proceed or [q] to quit > '
            )
            if optimise == "":
                break
            elif optimise == "q":
                print("quitting...")
                quit()
            elif int(optimise) > 0:
                result = sp.sp.recommendations(
                    seed_artists=seed, limit=limit, target_popularity=optimise
                )
                track_ids = SpotifyFetcher().print_and_process_response(result)
            else:  # no popularity target
                result = sp.sp.recommendations(seed_artists=seed, limit=limit)
                track_ids = SpotifyFetcher().print_and_process_response(result)

        return track_ids

    @staticmethod
    def print_and_process_response(result):
        """
        Processes and prints the response from the Spotify API call.

        This method takes the result from the Spotify API call and extracts the track IDs.
        It also prints the track information in a readable format for the user.

        Parameters:
            result (dict): The JSON response obtained from the Spotify API call.

        Returns:
            list of str: A list of track IDs extracted from the response.
        """
        track_ids = []
        for idx, track in enumerate(result["tracks"]):
            print(
                f"#{idx+1:02} | {track['artists'][0]['name']} - {track['name']} | pop: {track['popularity']}."
            )
            track_ids.append(track["id"])
        return track_ids
