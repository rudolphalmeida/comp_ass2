import sys

from harvesters import TwitterStreamer
from listeners import CouchDBListener, ToFileListener


AUS_GEO_RANGE = [112, -44, 155, -10]
GROUP_MEMBERS = ["RUD", "SAG", "SHE", "VIS", "SHA"]


for member in GROUP_MEMBERS:
    streamer = TwitterStreamer(
        member,
        # Hashtags and usernames to track
        # FIXME: This is not honoured
        # track=[
        #     "MasterChefAU",
        #     "masterchefaustralia",
        #     "masterchef",
        #     "SimonTohey",
        #     "tastingaustralia",
        #     "masterchef2020",
        #     "season12",
        #     "RoseAdamCooks",
        #     "sarahclarecooks",
        #     "S_Tiong",
        #     "SimonToohey",
        #     "TessaBoersma",
        #     "trackycollins_",
        #     "harry_fos",
        #     "hayden_quinn",
        #     "jesselemon",
        #     "khanhong",
        # ],
        track=["trump"],
        locations=AUS_GEO_RANGE,
    )
    stream = None
    try:
        # stream = streamer.stream(
        #     CouchDBListener("http://admin:password@127.0.0.1:5984/")
        # )
        stream = streamer.stream(ToFileListener(sys.stdout))
    except KeyboardInterrupt:
        print("Shutting down...")
        if stream is not None:
            stream.shutdown()
        sys.exit(0)
