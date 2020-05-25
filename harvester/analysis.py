import re

from textblob import TextBlob


def clean_tweet_text(tweet):
    return " ".join(
        re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()
    )


def sentiment(tweet):
    analysis = TextBlob(clean_tweet_text(tweet))

    if analysis.sentiment.polarity == 0:
        return 0  # Neutral
    elif analysis.sentiment.polarity < 1:
        return -1  # Negative
    else:
        return 1  # Positive
