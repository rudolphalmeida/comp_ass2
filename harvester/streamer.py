import logging
import json

from tweepy.streaming import StreamListener
from tweepy import Stream
import couchdb

import analysis


logging.basicConfig(
    filename="harvester.log",
    filemode="w",
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

    def on_status(self, status):
        logging.info("writing tweet to {}".format(self.file))

        data = None
        try:
            data = analysis.extract(status)
        except Exception as e:
            logging.info("exception in parsing tweet: {}".format(e))
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

    def on_status(self, status):
        logging.info("writing tweet to couchdb")
        data = None
        try:
            data = analysis.extract(status)
        except Exception as e:
            logging.info("exception in parsing tweet: {}".format(e))
            return True

        data["sentiment"] = analysis.sentiment(data["text"])
        self.db.save(json.dumps(data))

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
        "@DanielAndrewsMP",
        "#AnnastaciaMP",
        "#GladysB",
        "#MarkMcGowanMP",
        "#marshall_steven",
        "#PeterGutwein",
        "#ABarrMLA",
        "#fanniebay",
        "#DanielAndrewsMP",
        "#Annastacia",
        "#MarkMcGowan",
    ]

    user = "RUD"
    logging.info("scraping with user {}".format(user))

    stream_tweets(
        # auth=credentials.authenticate(user),
        # listener=ToFileListener(sys.stdout),
        # listener=ToFileListener(open("tweets.json", "a")),
        listener=CouchDBListener("http://admin:password@127.0.0.1:5984/"),
        track=track,
    )
