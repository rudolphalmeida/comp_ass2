import logging
import time
from collections import Counter
import json

from tweepy import API, error
import couchdb

import credentials
import analysis

logging.basicConfig(
    filename="scraper.log",
    filemode="w",
    level=logging.DEBUG,
    format="%(asctime)s %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
)

if __name__ == "__main__":
    track = "@AnnastaciaMP OR @GladysB OR @MarkMcGowanMP OR @marshall_steven OR @PeterGutwein OR @ABarrMLA OR @fanniebay OR @DanielAndrews OR #AnnastaciaMP OR #GladysB OR #MarkMcGowanMP OR #marshall_steven OR #PeterGutwein OR #ABarrMLA OR #fanniebay OR #DanielAndrews OR #MarkMcGowan OR #Annastacia"

    END_DATE = "2020-05-26"
    MAX_COUNT = 1000

    since_id = None
    max_id = None
    c = Counter()

    while True:

        # couch = couchdb.Server("http://admin:password@127.0.0.1:5984/")

        # try:
        #     db = couch["tweets"]  # Database already exists
        # except Exception:
        #     db = couch.create("tweets")

        limits = {"SAG": 1, "SHE": 1, "SHA": 1, "VIS": 1, "RUD": 1}

        for user in limits:
            logging.info("scraping with user {}".format(user))

            auth = credentials.authenticate(user)
            api = API(auth)

            while limits[user] > 0:
                try:
                    search_results = api.search(
                        q=track,
                        count=MAX_COUNT,
                        until=END_DATE,
                        include_entities=True,
                        lang="en",
                        since_id=since_id,
                        max_id=max_id,
                    )
                except error.TweepError:  # Should cover RateLimitException
                    logging.warning("exception in search")
                    break

                logging.info("found {} tweets".format(len(search_results)))

                if len(search_results) > 0:
                    id = None

                    for i, tweet in enumerate(search_results):
                        logging.info("saving tweet with id {}".format(tweet.id))
                        id = tweet.id

                        if i == 0:
                            max_id = id  # Save id of latest tweet in sequence

                        c[id] += 1
                        logging.info("writing tweet to database")
                        data = tweet._json
                        # Create partition id
                        # data["_id"] = "scrape:{}".format(data["id"])
                        data["sentiment"] = analysis.sentiment(data["text"])
                        # db.save(data)
                        print(data)

                    since_id = id  # Save id of the farthest tweet in sequence

                limits[user] = int(api.last_response.headers["x-rate-limit-remaining"])
                logging.info(
                    "rate limit remaining for {} is {}".format(user, limits[user])
                )

                print(c.most_common(10))

        logging.info("sleeping")
        time.sleep(16 * 60)
