import re

from textblob import TextBlob


names = {
    "Daniel_Andrews": ["danielandrewsmp", "danielndrews", "vicpremier"],
    "Annastacia_Palaszczuk": ["annastaciamp", "qldpremier"],
    "Gladys_Berejiklian": ["gladysb_mp", "gladysb", "nsw_premiew"],
    "Mark_McGowan": ["markmcgowanmp", "wapremier"],
    "Steven_Marshall": ["marshall_steven", "marshall_stevenmp", "sapremier"],
    "Peter_Gutwein": ["petergutwein", "petergutweinmp", "taspremier"],
}


def get_text(status):
    if hasattr(status, "retweeted_status"):  # Check if Retweet
        try:
            return status.retweeted_status.extended_tweet["full_text"]
        except AttributeError:
            return status.retweeted_status.text
    else:
        try:
            return status.extended_tweet["full_text"]
        except AttributeError:
            return status.text


def get_mentions_and_hashtags(status):
    res = []

    if hasattr(status, "extended_tweet"):
        for hashtag in status.extended_tweet.entities["hashtags"]:
            res.append(hashtag["text"].lower())

        for user in status.extended_tweet.entities["user_mentions"]:
            res.append(user["screen_name"].lower())
    else:
        for hashtag in status.entities["hashtags"]:
            res.append(hashtag["text"].lower())

        for user in status.entities["user_mentions"]:
            res.append(user["screen_name"].lower())

    return res


def mentions(tweet, name):
    mentions_and_hashtags = get_mentions_and_hashtags(tweet)

    candidates = names[name]

    for candidate in candidates:
        if candidate in mentions_and_hashtags:
            return 1
    return 0


def extract(status):
    clean_tweet = dict()

    clean_tweet["id"] = status.id
    clean_tweet["text"] = get_text(status)

    clean_tweet["Daniel_Andrews"] = mentions(status, "Daniel_Andrews")
    clean_tweet["Annastacia_Palaszczuk"] = mentions(status, "Annastacia_Palaszczuk")
    clean_tweet["Gladys_Berejiklian"] = mentions(status, "Gladys_Berejiklian")
    clean_tweet["Mark_McGowan"] = mentions(status, "Mark_McGowan")
    clean_tweet["Steven_Marshall"] = mentions(status, "Steven_Marshall")
    clean_tweet["Peter_Gutwein"] = mentions(status, "Peter_Gutwein")

    return clean_tweet


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
