#
# Verarbeitet die 'topics.txt' zu einer 'topics.json'
#

import json

topics = {}
current = ""
data = open("topics.txt", "r").read().split("\n")
for line in data:
    if (line.startswith("#")):
        current = line.split("# ")[1]
        topics[current] = {
            "keywords": []
        }
    if (line.startswith("-")):
        topics[current]["keywords"].append(line.split("- ")[1])

f = open("topics.json", "w").write(json.dumps(topics, indent=4))