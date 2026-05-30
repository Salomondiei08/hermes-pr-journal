import json
with open("data/tracked_prs.json") as f:
    data = json.load(f)
print(len(data))
