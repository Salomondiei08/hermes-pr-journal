import json
import sys
data = json.load(open(sys.argv[1]))
print(len(data.get("tracked_prs", data)))
