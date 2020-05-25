import logging
import time

from tweepy import API

import credentials

logging.basicConfig(
    filename="scraper.log",
    filemode="a",
    level=logging.DEBUG,
    format="%(asctime)s %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
)

if __name__ == "__main__":
    track = "@DanielAndrews"

    END_DATE = "2020-05-25"
    MAX_COUNT = 100

    while True:
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

                    with open("scraper.json", "a") as jsonFile:
                        for tweet in search_results:
                            logging.info("saving tweet with id {}", tweet.id)
                            id = tweet.id
                            logging.info("writing tweet to {}".format(jsonFile))
                            print(tweet._json, file=jsonFile)

                        since = id

                limits[user] = int(api.last_response.headers["x-rate-limit-remaining"])
                logging.info(
                    "rate limit remaining for {} is {}".format(user, limits[user])
                )

        logging.info("sleeping")
        time.sleep(16 * 60)
