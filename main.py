"""Get song titles and artists from Spotify playlist"""

import csv
import os
import re
import pandas as pd
from googleapiclient.discovery import build
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials

# load credentials from .env file
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID", "")
CLIENT_SECRET = os.getenv("CLIENT_SECRET", "")
OUTPUT_FILE_NAME = "tracks.csv"

# change for your target playlist
PLAYLIST_LINK = "https://open.spotify.com/playlist/6nGX6s6mecH0mJAyUUr2Ws?si=a39da8a7ccf3475e"



# authenticate
client_credentials_manager = SpotifyClientCredentials(
    client_id=CLIENT_ID, client_secret=CLIENT_SECRET
)
# create spotify session object
session = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
# get uri from https link
if match := re.match(r"https://open.spotify.com/playlist/(.*)\?", PLAYLIST_LINK):
    playlist_uri = match.groups()[0]
else:
    raise ValueError("Expected format: https://open.spotify.com/playlist/uri")
# get list of tracks in a given playlist (note: max playlist length 100)
tracks = session.playlist_tracks(playlist_uri)["items"]
# create csv file
with open(OUTPUT_FILE_NAME, "w", encoding="utf-8") as file:
    writer = csv.writer(file)
    # write header column names
    writer.writerow(["track", "artist"])
    # extract name and artist
    for track in tracks:
        name = track["track"]["name"]
        artists = ", ".join(
            [artist["name"] for artist in track["track"]["artists"]]
        )
        # write to csv
        writer.writerow([name, artists])
# Function to search YouTube
def youtube_search(track, artist, youtube_api_key):
    youtube = build('youtube', 'v3', developerKey=youtube_api_key)
    search_response = youtube.search().list(
        q=f"{track} {artist}",
        part='id,snippet',
        maxResults=1
    ).execute()
    if 'items' in search_response and search_response['items']:
        video_id = search_response['items'][0]['id']['videoId']
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        return video_url
    return None
# Load CSV file
input_csv = 'tracks.csv'  # Change this to your file path
tracks_df = pd.read_csv(input_csv)
# Add a column for YouTube links
tracks_df['YouTube Link'] = None
# Your YouTube API key
youtube_api_key = 'AIzaSyB38qnuta0hz27_uIXQ4wZFMQrL2dKRTVA'  # Replace with your YouTube API key
# Search for each track and artist
for index, row in tracks_df.iterrows():
    track = row['track']
    artist = row['artist']
    video_url = youtube_search(track, artist, youtube_api_key)
    tracks_df.at[index, 'YouTube Link'] = video_url
# Save the results to a new CSV file
output_csv = 'tracks_with_youtube_links.csv'
tracks_df.to_csv(output_csv, index=False)
print(f"Results saved to {output_csv}")




