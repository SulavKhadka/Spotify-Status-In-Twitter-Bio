import os
import sys
import json
import time
import webbrowser
import spotify_client
import twitter_client

def main(heroku=False):

    if heroku:
        try:
            refresh_token_offset_in_seconds = int(os.environ["refresh_token_offset_in_seconds"])
            bio_update_time_interval_in_seconds = int(os.environ["update_time_interval_in_seconds"])
            bio_update_time = int(time.time()) + bio_update_time_interval_in_seconds

            consumer_key = os.environ["twitter_consumer_key"]
            consumer_secret = os.environ["twitter_consumer_secret"]
            twitter = twitter_client.TwitterClient(consumer_key, consumer_secret)

            client_id = os.environ["spotify_client_id"]
            client_secret = os.environ["spotify_client_secret"]
            username = os.environ["spotify_username"]
            redirect_uri = os.environ["spotify_redirect_uri"]
            scope = os.environ["spotify_scope"]
            spotify = spotify_client.SpotifyClient(username, client_id, client_secret, redirect_uri, scope)
        except Exception as e:
            print("Failed to read env variables") 
            raise(e)
    else:
        with open("creds.json", "r") as file:
            script_variables = json.load(file)

        twitter_creds = script_variables.get("twitter")
        spotify_creds = script_variables.get("spotify")
        refresh_token_offset_in_seconds = script_variables.get("refresh_token_offset_in_seconds")
        bio_update_time_interval_in_seconds = script_variables.get("update_time_interval_in_seconds")
        bio_update_time = int(time.time()) + bio_update_time_interval_in_seconds

        if twitter_creds and spotify_creds:
            consumer_key = twitter_creds.get("consumer_key")
            consumer_secret = twitter_creds.get("consumer_secret")
            twitter = twitter_client.TwitterClient(consumer_key, consumer_secret)

            client_id = spotify_creds.get("client_id")
            client_secret = spotify_creds.get("client_secret")
            username = spotify_creds.get("username")
            redirect_uri = spotify_creds.get("redirect_uri")
            scope = spotify_creds.get("scope")
            spotify = spotify_client.SpotifyClient(username, client_id, client_secret, redirect_uri, scope) 
        
        else:
            print("Whoops")

    twitter.user_login()
    spotify.user_login()

    last_bio = ""

    while True:
        try:
            if int(time.time()) >= (spotify.token_refresh_time - refresh_token_offset_in_seconds):
                print("refreshing token...")
                spotify.refresh()

            if int(time.time()) >= bio_update_time:
                current_track = spotify.get_current_playing_track()
                if current_track:
                    bio = f"Currently listening to {current_track[0]} by {current_track[1]}."
                    if last_bio == bio:
                        pass
                        #print("Same bio. Not changing anything.")
                    else:
                        twitter.update_profile(bio)
                        last_bio = bio
                        print(f"Profile updated to:\n{bio}.")
                else:
                    print("Currently not listening to anything.")
                bio_update_time = int(time.time()) + bio_update_time_interval_in_seconds

                print(f"Time till spotify token refresh: {(spotify.token_refresh_time - refresh_token_offset_in_seconds) - int(time.time())}")
            else:
                pass
                # print(f"Not time to update yet. ~{bio_update_time - int(time.time())} seconds left.")
        except Exception as e:
            print("Bio not updated.")
            print(e)
            print("~~~~~~~~~~~~~~~~~~~~~")

        time.sleep(5)


main(heroku=True)   