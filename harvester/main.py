import sys

from harvesters import TwitterStreamer
from listeners import ToFileListener


streamer = TwitterStreamer("RUD")
streamer.stream(ToFileListener(sys.stdout), track=["#MasterChefAU"])
