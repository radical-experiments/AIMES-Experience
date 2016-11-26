import json
import sys


if len(sys.argv) != 2:
    print "This function takes a json file as input"
    sys.exit()

filename = sys.argv[1]

with open(filename) as j:
    j_file = json.load(j)

num_cu = len(j_file['unit'])
done_cu = 0

for cu in j_file['unit']:
    if "DONE" in cu['states']:
        done_cu += 1

if num_cu == done_cu:
    print "Successful run"
else:
    print "Unsuccessful run"
