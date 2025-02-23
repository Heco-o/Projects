import json
import time

with open("positions.json", "r") as file:
	data = file.read()
print("loading...")
a = time.time()
data = json.loads(data)
b = time.time()
print("Done! " + str(b - a) + "s")