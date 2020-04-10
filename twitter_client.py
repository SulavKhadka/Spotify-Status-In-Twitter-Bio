import json
import tweepy
import requests
import webbrowser

class TwitterClient:

    def __init__(self, consumer_key, consumer_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.api = ""


    def user_login(self):
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)

        # Redirect user to Twitter to authorize
        webbrowser.open_new_tab(auth.get_authorization_url())

        token = input("Enter code:")
        # Get access token
        auth.get_access_token(token)

        # Construct the API instance
        api = tweepy.API(auth)

        self.api = api


    def update_profile(self, bio):
        self.api.update_profile(description=bio)


if __name__ == "__main__":
    with open("creds.json", "r") as file:
        script_variables = json.load(file)

    twitter_creds = script_variables.get("twitter")

    if twitter_creds:
        consumer_key = twitter_creds.get("consumer_key")
        consumer_secret = twitter_creds.get("consumer_secret")
        twitter_client = TwitterClient(consumer_key, consumer_secret)
    else:
        print("Whoops")