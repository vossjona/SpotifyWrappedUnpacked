# SpotifyWrappedUnpacked
Spotify Wrapped is not detailed enough. Here, I explore my listening habits with the help of the Spotify Web API.

## Collect_recently_played_songs.py
Collects the following data for each song:
- Title
- Main Artist
- Album Name
- Genres associated with the main artist
- Length (in milliseconds)
- Popularity from 0 (unpopular) to 1 (super popular)
- Release Date of the album
- Context (the type of Spotify entity where the song was played)
- Explicit (True/False)
- Played at (the date and time when the song was played)

The script runs continuously, collecting data every 2 hours and saving it to a .csv file in the working directory.

### Dependencies
- Python 3
- pandas
- Authentification with the [Spotify Web API](https://developer.spotify.com/documentation/web-api)
- [Spotipy Wrapper](https://spotipy.readthedocs.io/en/2.22.1/)

### How to Use
1. Gain Cliend ID, Client Secret and Redirect URI from Spotify Web API.
2. In this version they are saved as environment variables, but you can easily pass them as normal variables.
3. Run script in your environment.
4. The collected data is saved into a CSV file named 'recently_played_songs.csv'.
5. After collection the script will go to sleep for 2 hours before collecting again.


## WrappedUnpacked.ipynb
Contains functions to collect information about the users
- top 50 tracks
- saved songs (all)
- recently played songs
