import logging

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

    auth = credentials.authenticate("SAG")
    api = API(auth)

    COUNT = 50000
    END_DATE = "2020-05-25"

    logging.info("scraping {} tweets until {}".format(COUNT, END_DATE))

    search_results = api.search(q=track, count=COUNT, until=END_DATE)

    with open("scraper.json", "a") as jsonFile:
        for tweet in search_results:
            logging.info("writing tweet to {}".format(jsonFile))
            print(tweet, file=jsonFile)
