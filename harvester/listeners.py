from tweepy.streaming import StreamListener
import couchdb


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
        self.db.save(raw_data)

    def on_error(self, status_code):
        if status_code == 420:  # Rate limit reached
            # Disconnect the stream
            return False
