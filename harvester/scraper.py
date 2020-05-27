import logging
from collections import Counter
import argparse

from tweepy import API, error, Cursor
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
    parser = argparse.ArgumentParser()
    parser.add_argument("cred_user")
    parser.add_argument("query", help="query to use for tracking")
    args = parser.parse_args()

    cred_user = args.cred_user
    query = args.query

    assert cred_user in ["SHE", "SAG", "SHA", "VIS", "SHE2"]

    # track = "@AnnastaciaMP OR @GladysB OR @MarkMcGowanMP OR @marshall_steven OR @PeterGutwein OR @ABarrMLA OR @fanniebay OR @DanielAndrews OR #AnnastaciaMP OR #GladysB OR #MarkMcGowanMP OR #marshall_steven OR #PeterGutwein OR #ABarrMLA OR #fanniebay OR #DanielAndrews OR #MarkMcGowan OR #Annastacia"

    MAX_COUNT = 1000

    c = Counter()

    # couch = couchdb.Server("http://admin:password@127.0.0.1:5984/")

    # try:
    #     db = couch["tweets"]  # Database already exists
    # except Exception:
    #     db = couch.create("tweets")

    logging.info("scraping with user {}".format(cred_user))
    logging.info("using query {}".format(query))

    auth = credentials.authenticate(cred_user)
    api = API(auth, wait_on_rate_limit=True)

    search_results = Cursor(
        api.search, q=query, count=MAX_COUNT, include_entities=True
    ).items(5000000)

    try:
        for tweet in search_results:
            logging.info("saving tweet with id {}".format(tweet.id))

            c[tweet.id] += 1
            logging.info("writing tweet to database")

            try:
                data = analysis.extract(tweet._json)
            except Exception as e:
                logging.info("exception in extract: {}".format(e))
                continue
            data["sentiment"] = analysis.sentiment(data["text"])

            # db.save(data)
            print(data)
    except error.TweepError as e:  # Should cover RateLimitException
        logging.error("exception in search_results: {}".format(e))
        logging.info("exiting...")
    except Exception:
        logging.info("shutting down...")

    print(c.most_common(10))
