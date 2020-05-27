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


def get_mentions_and_hashtags(entities):
    res = []

    hashtags = entities["hashtags"]
    for hashtag in hashtags:
        res.append(hashtag["text"].lower())

    user_mentions = entities["user_mentions"]
    for user in user_mentions:
        res.append(user["screen_name"].lower())

    return res


def get_full_text(status):
    try:
        return status.retweeted_status.full_text
    except AttributeError:  # Not a Retweet
        return status.full_text


def mentions(tweet, name):
    mentions_and_hashtags = get_mentions_and_hashtags(
        tweet["entities"]
        if not tweet.get("truncated", False)
        else tweet["extended_tweet"]["entities"]
    )

    candidates = names[name]

    for candidate in candidates:
        if candidate in mentions_and_hashtags:
            return 1
    return 0


def extract(tweet):
    clean_tweet = dict()

    clean_tweet["id"] = tweet.id
    clean_tweet["text"] = get_full_text(tweet)

    print(clean_tweet["text"])

    clean_tweet["Daniel_Andrews"] = mentions(tweet, "Daniel_Andrews")
    clean_tweet["Annastacia_Palaszczuk"] = mentions(tweet, "Annastacia_Palaszczuk")
    clean_tweet["Gladys_Berejiklian"] = mentions(tweet, "Gladys_Berejiklian")
    clean_tweet["Mark_McGowan"] = mentions(tweet, "Mark_McGowan")
    clean_tweet["Steven_Marshall"] = mentions(tweet, "Steven_Marshall")
    clean_tweet["Peter_Gutwein"] = mentions(tweet, "Peter_Gutwein")

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
