from tweepy import API
from tweepy import Cursor
from tweepy import Stream

import credentials


class TwitterScraper:
    """
    Class to scrape the latest tweets off a particular users timeline
    """

    def __init__(self, auth_name):
        self.auth = credentials.authenticate(auth_name)
        self.client = API(self.auth)

    # username is the username without the prefix `@`
    def get_timeline_tweets(self, username, num_tweets):
        tweets = [
            tweet
            for tweet in Cursor(self.client.user_timeline, id=username).items(
                num_tweets
            )
        ]
        return tweets


class TwitterStreamer:
    """
    Class to stream the latest tweets on some particular topic
    """

    def __init__(self, auth_name, track, locations):
        self.auth = credentials.authenticate(auth_name)
        self.track = track
        self.locations = locations

    def stream(self, listener):
        tweet_stream = Stream(self.auth, listener)
        tweet_stream.filter(track=self.track, locations=self.locations)

    def async_stream(self, listener):
        tweet_stream = Stream(self.auth, listener)
        tweet_stream.filter(track=self.track, locations=self.locations, is_async=True)
