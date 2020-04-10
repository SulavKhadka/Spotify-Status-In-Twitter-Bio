import json
import time
import webbrowser
import spotipy
import spotipy.util as util
from spotipy import oauth2
from pprint import pprint

class SpotifyClient:

    def __init__(self, username, client_id, client_secret, redirect_uri, scopes):
        self.username = username
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scopes = scopes
        self.OAuth = None
        self.sp = None
        self.token_refresh_time = None


    def user_login(self):

        self.OAuth = oauth2.SpotifyOAuth(client_id=self.client_id,client_secret=self.client_secret,redirect_uri=self.redirect_uri,scope=self.scopes, username=self.username)
        self.token = self.OAuth.get_cached_token() 
        if not self.token:
            auth_url = self.OAuth.get_authorize_url()
            webbrowser.open_new_tab(auth_url)
            response = input('Paste the redirect url here: ')

            code = self.OAuth.parse_response_code(response)
            self.token = self.OAuth.get_access_token(code)

        self.sp = spotipy.Spotify(auth=self.token['access_token'])
        self.token_refresh_time = int(time.time()) + self.token['expires_in']


    def refresh(self):
        if self.OAuth.is_token_expired(self.token):
            self.token = self.OAuth.refresh_access_token(self.token['refresh_token'])
            print(self.token)
            self.sp = spotipy.Spotify(auth=self.token['access_token'])
            self.token_refresh_time = int(time.time()) + self.token['expires_in']

    def get_current_playing_track(self):
        self.sp = spotipy.Spotify(auth=self.token['access_token'])
        results = self.sp.current_user_playing_track()
        try:
            item = results.get("item")
            artist = item["artists"][0]["name"]
            name = item.get("name")
            return(name, artist)
        except:
            return None


if __name__ == "__main__":
    with open("creds.json", "r") as file:
        script_variables = json.load(file)

    spotify_creds = script_variables.get("spotify")

    if spotify_creds:
        client_id = spotify_creds.get("client_id")
        client_secret = spotify_creds.get("client_secret")
        username = spotify_creds.get("username")
        redirect_uri = spotify_creds.get("redirect_uri")
        scope = spotify_creds.get("scope")

        spotify_client = SpotifyClient(username, client_id, client_secret, redirect_uri, scope) 
    else:
        print("Whoops")