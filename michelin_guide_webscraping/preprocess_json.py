import json

with open('./michelin_guide_webscraping/restaurant_scrapped.json', 'r') as json_file:
    data_dict = json.load(json_file)

preprocessed_dict = []
i = 0
for row in range(len(data_dict)):
    for element in range(len(data_dict[row]["restaurant-name"])):
        preprocessed_dict.append({})
        preprocessed_dict[i]["restaurant-name"] = data_dict[row]["restaurant-name"][element]
        preprocessed_dict[i]["restaurant-region"] = data_dict[row]["restaurant-region"][element]
        preprocessed_dict[i]["restaurant-city"] = data_dict[row]["restaurant-city"][element]
        preprocessed_dict[i]["restaurant-distinction"] = data_dict[row]["restaurant-distinction"][element]
        preprocessed_dict[i]["restaurant-chef"] = data_dict[row]["restaurant-chef"][element]
        preprocessed_dict[i]["restaurant-cooking-type"] = data_dict[row]["restaurant-cooking-type"][element]
        preprocessed_dict[i]["restaurant-menu-price"] = data_dict[row]["restaurant-menu-price"][element]
        i+=1

file_path = './michelin_guide_webscraping/restaurant_cleaned.json'
with open(file_path, "w") as json_file:
    json.dump(preprocessed_dict, json_file, indent=4)
