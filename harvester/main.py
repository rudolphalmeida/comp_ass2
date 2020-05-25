import json
import sys
import logging

from tweepy.streaming import StreamListener
from tweepy import Stream
import couchdb

import credentials


logging.basicConfig(filename="harvester.log", filemode="a", level=logging.DEBUG)


class ToFileListener(StreamListener):
    """
    A stream listener that just prints the tweets to file
    """

    def __init__(self, file, api=None):
        self.file = file
        super().__init__(api=api)

    def on_data(self, raw_data):
        logging.info("writing tweet to {}".format(self.file))
        print(raw_data, file=self.file, end=",")
        return True

    def on_error(self, status_code):
        logging.warning("received status code {}".format(status_code))
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
        logging.info("connected to couchdb database")
        super().__init__(api=api)

    def on_data(self, raw_data):
        logging.info("writing tweet to couchdb")
        self.db.save(json.loads(raw_data))

    def on_error(self, status_code):
        logging.warning("received status code {}".format(status_code))
        if status_code == 420:  # Rate limit reached
            # Disconnect the stream
            return False


def stream_tweets(auth, listener, track):
    logging.info("beginning streaming")
    stream = Stream(auth, listener)
    stream.filter(track=track)


if __name__ == "__main__":
    track = ["@DanielAndrewsMP"]

    for user in ["RUD", "SAG"]:
        logging.info("using {} credentials for streaming".format(user))
        stream_tweets(
            auth=credentials.authenticate(user),
            listener=ToFileListener(open("tweets.json", "a")),
            track=track,
        )
