from json import *

with open('accommodation/finlib.json', 'r') as f:
    data = load(f)


grouped_data = {}

for obj in data:
    keys = obj.keys()
    city = list(keys)[0]
    category = list(obj[city].keys())[0]
    if city not in grouped_data:
        grouped_data[city] = {}
    if category not in grouped_data[city]:
        grouped_data[city][category] = {}
    one = list(obj[city][category].keys())[0]
    if one != "name":
        if one not in grouped_data[city][category]:
            grouped_data[city][category][one] = {}
        two = list(obj[city][category][one].keys())[0]
        if two != "name":
            if two not in grouped_data[city][category][one]:
                grouped_data[city][category][one][two] = {}
            three = list(obj[city][category][one][two].keys())[0]
            if three != "name":
                if three not in grouped_data[city][category][one][two]:
                    grouped_data[city][category][one][two][three] = []
                grouped_data[city][category][one][two][three].append(
                    obj[city][category][one][two][three])
            else:
                two_list = two + " list"
                if two_list not in grouped_data[city][category][one][two]:
                    grouped_data[city][category][one][two][two_list] = []
                grouped_data[city][category][one][two][two_list].append(
                    obj[city][category][one][two])

        else:
            one_list = one + " list"
            if one_list not in grouped_data[city][category][one]:
                grouped_data[city][category][one][one_list] = []
            grouped_data[city][category][one][one_list].append(
                obj[city][category][one])

    else:
        category_list = category + " list"
        if category_list not in grouped_data[city][category]:
            grouped_data[city][category][category_list] = []
        grouped_data[city][category][category_list].append(obj[city][category])

print(len(grouped_data))

with open('grouped_file.json', 'w') as f:
    dump(grouped_data, f, indent=2)
