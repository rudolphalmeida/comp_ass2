import tweepy
from tweepy.streaming import StreamListener

import credentials


class ToFileListener(StreamListener):
    """
    A stream listener that just prints the tweets to file
    """

    def __init__(self, file, api=None):
        self.file = file
        super().__init__(api=api)

    def on_data(self, raw_data):
        print(raw_data)
        print(raw_data, file=self.file)
        return True

    def on_error(self, status_code):
        print(status_code)


class CouchDBListener(StreamListener):
    """
    A stream listener that extracts relevant information from tweets and
    stores them to the configured CouchDB instance
    """

    def on_data(self, raw_data):
        return super().on_data(raw_data)

    def on_error(self, status_code):
        return super().on_error(status_code)


if __name__ == "__main__":
    auth = tweepy.OAuthHandler(credentials.RUD_CONS_KEY, credentials.RUD_CONS_SECRET)
    auth.set_access_token(
        credentials.RUD_TOKEN, credentials.RUD_TOKEN_SECRET,
    )

    listener = ToFileListener(open("tweets.json", "w"))
    stream = tweepy.Stream(auth, listener)

    stream.filter(track=["#MasterChefAU"])
