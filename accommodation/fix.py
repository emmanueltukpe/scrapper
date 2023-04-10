from json import *

with open('finlib.json', 'r') as f:
    data = load(f)

grouped_data = {}

for obj in data:
    key = list(obj.keys())[0]
    if key in grouped_data:
        grouped_data[key].append(obj[key])
    else:
        grouped_data[key] = [obj[key]]

with open('grouped_file.json', 'w') as f:
    dump(grouped_data, f, indent=2)
