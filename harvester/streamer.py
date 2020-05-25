import json
import logging
import time
import sys

from tweepy.streaming import StreamListener
from tweepy import Stream
import couchdb

import credentials
import analysis


logging.basicConfig(
    filename="harvester.log",
    filemode="a",
    level=logging.DEBUG,
    format="%(asctime)s %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
)


class ToFileListener(StreamListener):
    """
    A stream listener that just prints the tweets to file
    """

    def __init__(self, file, api=None):
        self.file = file
        super().__init__(api=api)

    def on_data(self, raw_data):
        logging.info("writing tweet to {}".format(self.file))
        data = json.loads(raw_data)
        # Create partition id
        # data["_id"] = "stream:{}".format(data["id"])
        if "text" not in data:
            return True

        data["sentiment"] = analysis.sentiment(data["text"])
        print(data, file=self.file)
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
            self.db = couch["tweets"]  # Table is created
        except Exception:
            self.db = couch.create("tweets")
        logging.info("connected to couchdb database")
        super().__init__(api=api)

    def on_data(self, raw_data):
        logging.info("writing tweet to couchdb")
        data = json.loads(raw_data)
        # Create partition id
        # data["_id"] = "stream:{}".format(data["id"])
        data["sentiment"] = analysis.sentiment(data["text"])
        self.db.save(data)

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
    track = [
        "@AnnastaciaMP",
        "@GladysB",
        "@MarkMcGowanMP",
        "@marshall_steven",
        "@PeterGutwein",
        "@ABarrMLA",
        "@fanniebay",
        "@DanielAndrews",
        "#AnnastaciaMP",
        "#GladysB",
        "#MarkMcGowanMP",
        "#marshall_steven",
        "#PeterGutwein",
        "#ABarrMLA",
        "#fanniebay",
        "#DanielAndrews",
        "#Annastacia",
        "#MarkMcGowan",
    ]

    limits = {"RUD": 1, "SAG": 1, "SHE": 1, "SHA": 1, "VIS": 1}

    while True:
        for user in limits:
            logging.info("scraping with user {}".format(user))

            stream_tweets(
                auth=credentials.authenticate(user),
                # listener=ToFileListener(sys.stdout),
                # listener=ToFileListener(open("tweets.json", "a")),
                listener=CouchDBListener("http://admin:password@127.0.0.1:5984/"),
                track=track,
            )

            logging.info("rate limit reached for {}".format(user))

        time.sleep(16 * 60)
