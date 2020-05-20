from tweepy.streaming import StreamListener


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

    def on_data(self, raw_data):
        return super().on_data(raw_data)

    def on_error(self, status_code):
        if status_code == 420:  # Rate limit reached
            # Disconnect the stream
            return False
