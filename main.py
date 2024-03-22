from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

date_input = input("Enter the date for which you would like to see the top 100 charts(YYYY-MM-DD): ")

url = requests.get(f"https://www.billboard.com/charts/hot-100/{date_input}/")

soup = BeautifulSoup(url.text, "html.parser")

songs = soup.select("li ul li h3")

songs_list = [song.getText().strip() for song in songs]

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id="client_id",
        client_secret="client_secret",
        cache_path="token.txt",
        redirect_uri="http://example.com",
        show_dialog=True,
        scope="playlist-modify-private",
        username="username"
    )
)

user_id = sp.current_user()["id"]
song_uris = []
year = date_input.split("-")[0]

for song in songs_list:
    song_details = sp.search(q=f"track:{song} year:{year}", type="track")
    print(song_details)
    try:
        uri = song_details["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} not found.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date_input} billboard 100", public=False)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)

