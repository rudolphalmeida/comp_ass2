import json


votes = {
    "VIC": {"Labor": 0, "Liberal": 0},
    "NSW": {"Labor": 0, "Liberal": 0},
    "ACT": {"Labor": 0, "Liberal": 0},
    "WA": {"Labor": 0, "Liberal": 0},
    "NT": {"Labor": 0, "Liberal": 0},
    "QLD": {"Labor": 0, "Liberal": 0},
    "TAS": {"Labor": 0, "Liberal": 0},
    "SA": {"Labor": 0, "Liberal": 0},
}

data = None
with open("data.json", "r") as json_file:
    data = json.load(json_file)

for polling_station in data["features"]:
    state = polling_station["properties"]["state"]
    tally = votes[state]

    tally["Labor"] += polling_station["properties"]["tpp_australian_labor_party_votes"]
    tally["Liberal"] += polling_station["properties"][
        "tpp_liberal_national_coalition_votes"
    ]

for state, tally in votes.items():
    print("In state {}: ".format(state), end="")
    if tally["Labor"] > tally["Liberal"]:
        print("{}".format("Labor"))
        votes[state]["winner"] = "Labor"
    else:
        print("{}".format("Liberal"))
        votes[state]["winner"] = "Liberal"

print(json.dumps(votes))
