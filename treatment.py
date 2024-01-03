import json
import pandas as pd
import re

def load_json(path):
    """load the configuration file"""
    with open(path, 'r') as file:
        data = json.load(file)
    return data

def deep_normalization(string):
    string = string.lower()
    string = string.replace('\n', '').strip()
    string = string.replace('é', 'e').replace('è', 'e').replace('ê', 'e').replace('ë', 'e')
    string = string.replace('î', 'i').replace('ô', 'o').replace('ï', 'i').replace('ö', 'o').replace('œ', 'oe')
    string = string.replace('â', 'a').replace('ä', 'a').replace('û', 'u').replace('ü', 'u')
    string = re.sub(r'[^a-zA-Z0-9\s]', ' ', string) #for the ' " - _  etc...
    return string

def treat_data_wikidata(data):
    distinctions = []
    chefs = []
    for line in data :
        chef = line["chefLabel"]
        if not chef in chefs:
            chefs.append(chef)

        if len(line) > 1:
            distinction = line["distinctionLabel"]
            if not distinction in distinctions:
                distinctions.append(distinction)
    
    dict = {}
    for chef in chefs:
        dict[chef] = {}
        for distinction in distinctions:
            dict[chef][distinction] = False

    for line in data:
        chef = line["chefLabel"]
        if len(line) > 1:
            distinction = line["distinctionLabel"]
            dict[chef][distinction] = True

    df = pd.DataFrame(dict).transpose()
    return df

def treat_data_michelin(data):
    dict = {}
    for restaurant in data :
        name = restaurant["restaurant-name"]
        dict[name] = {}
        dict[name]["chef"] = restaurant["restaurant-chef"]
        dict[name]["region"] = restaurant["restaurant-region"]
        dict[name]["city"] = restaurant["restaurant-city"]
        dict[name]["star"] = restaurant["restaurant-distinction"]
        dict[name]["cooking_type"] = restaurant["restaurant-cooking-type"]
        dict[name]["price_range"] = restaurant["restaurant-menu-price"]
        
    df = pd.DataFrame(dict).transpose()
    return df

def treat_data_wikipedia(data):
    dict = {}
    for restaurant in data:
        name = restaurant["restaurant-name"].rstrip('\n')
        dict[name] = {}
        dict[name]["chef"] = restaurant["restaurant-chef"].rstrip('\n')
        dict[name]["region"] = restaurant["restaurant-region"]
        dict[name]["city"] = restaurant["restaurant-city"]
        dict[name]["star"] = restaurant["restaurant-distinction"]

    df = pd.DataFrame(dict).transpose()
    return df

def merging(wikidata_df, michelin_df, wikipedia_df):
    chefs_wikipedia = wikipedia_df["chef"].apply(deep_normalization)
    chefs_wikidata = wikidata_df.index.to_series().apply(deep_normalization)
    chefs_michelin = michelin_df["chef"].apply(deep_normalization)
    diff = chefs_wikipedia[~chefs_wikipedia.isin(chefs_michelin)]
    common = chefs_wikipedia[chefs_wikipedia.isin(chefs_michelin)]
    print(common)
    print(diff)
    return None


def main():
    path_wikidata = r"wikidata_chefs/chefs.json"
    data = load_json(path_wikidata)
    df_wikidata = treat_data_wikidata(data)

    path_michelin = r"michelin_guide_webscraping/restaurant_cleaned.json"
    data = load_json(path_michelin)
    df_michelin = treat_data_michelin(data)

    path_wikipedia = r'wikipedia_michelin_stars/two_three_stars_restaurant_cleaned.json'
    data = load_json(path_wikipedia)
    df_wikipedia = treat_data_wikipedia(data)

    merging(df_wikidata, df_michelin, df_wikipedia)

if __name__ == '__main__':
    main()