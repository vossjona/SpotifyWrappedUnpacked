
#%% Imports
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import pandas as pd
from datetime import datetime
import time
import sys
import keyboard

#%% Functions
def authenticate_spotify():
    """
    Uses environment variables to gain access to Spotify API
    
    Environment variables:
    SPOTIPY_CLIENT_ID
    SPOTIPY_CLIENT_SECRET
    SPOTIPY_REDIRECT_URI

    All found on the Spotify Developers Dashboard:
    https://developer.spotify.com/dashboard/20f128d8178c4ba3b89f4adf4e495b44/settings
    
    Returns:
        spotipy.Spotify instance that interacts with Spotify API
    """
    scope = ['playlist-read-private', 'user-read-recently-played', 'user-top-read', 'user-library-read']
    spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=os.getenv('SPOTIPY_CLIENT_ID'),
        client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
        redirect_uri=os.getenv('SPOTIPY_REDIRECT_URI'),
        scope=scope))
    
    return spotify

def convert_datetime_string_to_milliseconds(datetime_str):
    """
    Converts a datetime string in the format '%Y-%m-%dT%H:%M:%S.%fZ' to milliseconds.

    Args:
        datetime_str (str): The datetime string to convert.

    Returns:
        int: The datetime converted to milliseconds.
    """
    datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S.%fZ')
    milliseconds = int(time.mktime(datetime_obj.timetuple()) * 1000)
    return milliseconds

def fetch_last_function_call():
    """
    Fetches the last function call timestamp and date from a CSV file with information about songs.

    Returns:
        last_function_call_ms (int): The timestamp of the last function call in milliseconds.
        date_time_string (str): The date and time of the last function call.
    """
    with open('recently_played_songs.csv', 'r', errors='ignore') as csvfile:
        last_row = csvfile.readlines()[-1]
        
    date_time_string = last_row.split(',')[-1].replace('\n', '')
    last_function_call_ms = convert_datetime_string_to_milliseconds(date_time_string)
    return last_function_call_ms, date_time_string

def get_recently_played_songs(spotify):
    """
    Retrieves the recently played songs from Spotify for the current user.

    Args:
        spotify: The Spotify API object used for making API requests.

    Returns:
        A list of recently played songs, where each song is represented as a list containing the following information:
        - Song name
        - Artist name
        - Album name
        - Genres
        - Length (in milliseconds)
        - Popularity
        - Release date
        - Context (e.g., playlist, album, saved)
        - Explicit flag (True or False)
        - Played at (timestamp)

    """
    tracks = []
    after, date_time_string = fetch_last_function_call()
    recently_played_songs = spotify.current_user_recently_played(limit=50, after=after)
    # print('check')
        
    for item in recently_played_songs['items']:
        song_name = item['track']['name']
        print(song_name)
        played_at = item['played_at'] 
        if played_at == date_time_string:
            print('**Reached last song of previous call. Stopping here...')
            break
        album_name = item['track']['album']['name']
        release_date = item['track']['album']['release_date']
        first_artist_id = item['track']['artists'][0]['id']
        first_artist = spotify.artist(first_artist_id)
        first_artist_name = first_artist['name']
        artists = []
        for artist in item['track']['artists']:
            artists.append(artist['name'])
        genres = first_artist['genres']
        length = item['track']['duration_ms']
        popularity = item['track']['popularity']
        try:
            context = item['context']['type']
        except TypeError:
            context = 'saved'
        explicit = item['track']['explicit']

        tracks.append([song_name, artists, album_name, genres, length, popularity, release_date, context, explicit, played_at])

    return tracks

#%% Main
if __name__ == "__main__":
    while True:
        print('**Collecting...')
        spotify = authenticate_spotify()
        recently_played_songs = get_recently_played_songs(spotify)
        recently_played_songs_df = pd.DataFrame(recently_played_songs, columns=['Title', 'Artists', 'Album', 'Genre', 'Length (ms)', 'Popularity', 'Release Date', 'Context', 'Explicit', 'Played at'])
        recently_played_songs_df.sort_values('Played at', axis=0, ascending=True, inplace=True)
        try:
            recently_played_songs_df.to_csv('recently_played_songs.csv', mode='a', encoding='utf-8-sig', header=False, index=False)
        except PermissionError:
            print('**The csv file seems to be open. Please close it and try again.')
            sys.exit()
        print('**Going to sleep for 2 hours...')
        time.sleep(2*60*60) # Sleep for 2 hours
