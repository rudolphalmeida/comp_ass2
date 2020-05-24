import json
import sys

from tweepy.streaming import StreamListener
from tweepy import Stream
import couchdb

import credentials


class ToFileListener(StreamListener):
    """
    A stream listener that just prints the tweets to file
    """

    def __init__(self, file, api=None):
        self.file = file
        super().__init__(api=api)

    def on_data(self, raw_data):
        print(raw_data, file=self.file)
        return True

    def on_error(self, status_code):
        if status_code == 420:  # Rate limit reached
            # Disconnect the stream
            return False


class CouchDBListener(StreamListener):
    """
    A stream listener that extracts relevant information from tweets and
    stores them to the configured CouchDB instance
    """

    def __init__(self, server_id, api=None):
        couch = couchdb.Server(server_id)
        try:
            self.db = couch.create("tweets")
        except Exception:
            self.db = couch["tweets"]  # Table is created
        super().__init__(api=api)

    def on_data(self, raw_data):
        self.db.save(json.loads(raw_data))

    def on_error(self, status_code):
        if status_code == 420:  # Rate limit reached
            # Disconnect the stream
            return False


def stream_tweets(auth, listener, track):
    stream = Stream(auth, listener)
    stream.filter(track=track)


if __name__ == "__main__":
    # AUS_GEO_RANGE = [112, -44, 155, -10]

    # Authenticate using config.py and connect to Twitter Streaming API.
    track = [
        "#MasterChefAU",
        "#masterchefaustralia",
        "#masterchef",
        "#SimonToohey",
        "#tastingaustralia",
        "#masterchef2020",
        "#season12",
        "@RoseAdamCooks",
        "@sarahclarecooks",
        "@S_Tiong",
        "@SimonToohey",
        "@TessaBoersma",
        "@trackycollins_",
        "@harry_fos",
        "@hayden_quinn",
        "@jesselemon",
        "@khanhong",
    ]
    stream_tweets(
        auth=credentials.authenticate("RUD"),
        listener=ToFileListener(sys.stdout),
        track=track,
    )
