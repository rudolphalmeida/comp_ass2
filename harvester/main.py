import sys

from harvesters import TwitterStreamer
from listeners import ToFileListener


AUS_GEO_RANGE = [112, -44, 155, -10]
GROUP_MEMBERS = ["RUD", "SAG", "SHE", "VIS", "SHA"]


for member in GROUP_MEMBERS:
    streamer = TwitterStreamer(member)
    streamer.stream(
        ToFileListener(sys.stdout),
        track=[
            "#MasterChefAU",
            "#masterchefaustralia",
            "#masterchef",
            "#Chef",
            "#SimonTohey",
            "#tastingaustralia",
            "#masterchef2020",
            "#season12",
        ],
        locations=AUS_GEO_RANGE,
    )
