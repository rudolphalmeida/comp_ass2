import logging
import time
import json

from tweepy import API
import couchdb

import credentials
import analysis

logging.basicConfig(
    filename="scraper.log",
    filemode="a",
    level=logging.DEBUG,
    format="%(asctime)s %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
)

if __name__ == "__main__":
    track = "@AnnastaciaMP OR @GladysB OR @MarkMcGowanMP OR @marshall_steven OR @PeterGutwein OR @ABarrMLA OR @fanniebay OR @DanielAndrews OR #AnnastaciaMP OR #GladysB OR #MarkMcGowanMP OR #marshall_steven OR #PeterGutwein OR #ABarrMLA OR #fanniebay OR #DanielAndrews OR #MarkMcGowan OR #Annastacia"

    END_DATE = "2020-05-25"
    MAX_COUNT = 100

    while True:

        couch = couchdb.Server("http://admin:password@127.0.0.1:5984/")

        try:
            db = couch["tweets"]  # Database already exists
        except Exception:
            db = couch.create("tweets")

        since = None

        limits = {"RUD": 1, "SAG": 1, "SHE": 1, "SHA": 1, "VIS": 1}

        for user in limits:
            logging.info("scraping with user {}".format(user))

            auth = credentials.authenticate(user)
            api = API(auth)

            while limits[user] > 0:
                search_results = api.search(
                    q=track,
                    count=MAX_COUNT,
                    until=END_DATE,
                    include_entities=True,
                    lang="en",
                    since_id=since,
                )

                logging.info("found {} tweets".format(len(search_results)))

                if len(search_results) > 0:
                    id = None

                    for tweet in search_results:
                        logging.info("saving tweet with id {}".format(tweet.id))
                        id = tweet.id
                        logging.info("writing tweet to database")
                        data = tweet._json
                        # Create partition id
                        # data["_id"] = "scrape:{}".format(data["id"])
                        data["sentiment"] = analysis.sentiment(data["text"])
                        db.save(data)

                        since = id

                limits[user] = int(api.last_response.headers["x-rate-limit-remaining"])
                logging.info(
                    "rate limit remaining for {} is {}".format(user, limits[user])
                )

        logging.info("sleeping")
        time.sleep(16 * 60)
