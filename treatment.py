import json
import pandas as pd
import re


# Function to load a JSON file
def load_json(path):
    """load the configuration file"""
    with open(path, 'r') as file:
        data = json.load(file)
    return data


# Function for deep string normalization
def deep_normalization(string):
    string = string.lower()
    string = string.replace('\n', '').strip()
    # Replace specific characters with their normalized counterparts
    string = re.sub(r'[éèêëęėē]', 'e', string)
    string = re.sub(r'[àâªáäãåā]', 'a', string)
    string = re.sub(r'[îïìíįī]', 'i', string)
    string = re.sub(r'[ôºöòóõøō]', 'o', string)
    string = re.sub(r'[ûùüúū]', 'u', string)
    string = re.sub(r'[ñ,ń]', 'n', string)
    string = re.sub(r'[çćč]', 'c', string)
    string = re.sub('œ', 'oe', string)
    string = re.sub('æ', 'ae', string)
    string = re.sub(r'[^a-zA-Z0-9\s]', ' ', string) #for the ' " - _  etc...
    string = re.sub(r'\s+', ' ', string)
    return string


# Function to process data from Wikidata
def treat_data_wikidata(data):
    distinctions = []
    chefs = []
    for line in data :
        chef = deep_normalization(line["chefLabel"])
        if not chef in chefs:
            chefs.append(chef)

        if "distinctionLabel" in line:
            distinction = deep_normalization(line["distinctionLabel"])
            if not distinction in distinctions:
                distinctions.append(distinction)

    dict = {}
    for chef in chefs:
        dict[chef] = {}
        dict[chef]["birth-date"] = ""
        dict[chef]["death-date"] = ""
        for distinction in distinctions:
            dict[chef][distinction] = False

    for line in data:
        chef = deep_normalization(line["chefLabel"])
        if "birthdate" in line : 
            dict[chef]["birth-date"] = line["birthdate"]
        if "deathdate" in line :
            dict[chef]["death-date"] = line["deathdate"]
        if "distinctionLabel" in line:
            distinction = deep_normalization(line["distinctionLabel"])
            dict[chef][distinction] = True

    df = pd.DataFrame(dict).transpose()
    return dict, df


# Function to process data from the Michelin Guide
def treat_data_michelin(data):
    dict = {}
    nameskeys = ["chef", "region", "city", "distinction", "cooking-type", "menu-price"]
    for restaurant in data :
        name = deep_normalization(restaurant["restaurant-name"])
        dict[name] = {key: deep_normalization(restaurant['restaurant-' + key]) for key in nameskeys}
        
    df = pd.DataFrame(dict).transpose()
    return dict, df


# Function to process data from Wikipedia
def treat_data_wikipedia(data):
    dict = {}
    nameskeys = ["chef", "region", "city", "distinction"]
    for restaurant in data:
        name = deep_normalization(restaurant["restaurant-name"])
        dict[name] = {key: deep_normalization(restaurant['restaurant-' + key]) for key in nameskeys}
        
    df = pd.DataFrame(dict).transpose()
    return dict, df


# Function to merge data from different sources
def merging(wikidata_df, michelin_df, wikipedia_df, wikidata_dict, michelin_dict, wikipedia_dict):
    restaurants_dict = {}
    chefs_dict = {}
    keys = ["current-chef", "starred-chef", "region", "city", "distinction", "cooking-type", "menu-price"]
    michelin_keys = ["region", "city", "distinction", "cooking-type", "menu-price"]
    for restaurant in michelin_dict :
        restaurants_dict[restaurant] = {key: michelin_dict[restaurant][key] for key in michelin_keys}
        restaurants_dict[restaurant]["current-chef"] = michelin_dict[restaurant]["chef"]
        restaurants_dict[restaurant]["starred-chef"] = ""

    print("Restaurants invetored by Wikipedia that did not have found their twin in the Michelin Guide DataBase:")
    for i, wiki_rest in enumerate(wikipedia_dict): 
        flag = False
        wiki_pattern = re.compile(r'\b{}\b'.format(re.escape(wiki_rest)))
        for j, michelin_rest in enumerate(michelin_dict):
            michelin_pattern = re.compile(r'\b{}\b'.format(re.escape(michelin_rest)))
            if re.search(wiki_pattern, michelin_rest) and wikipedia_dict[wiki_rest]["distinction"] == michelin_dict[michelin_rest]["distinction"] and not flag:
                flag = True
                restaurants_dict[michelin_rest]["starred-chef"] = wikipedia_dict[wiki_rest]["chef"]

            elif re.search(michelin_pattern, wiki_rest) and wikipedia_dict[wiki_rest]["distinction"] == michelin_dict[michelin_rest]["distinction"] and not flag:
                flag = True 
                restaurants_dict[michelin_rest]["starred-chef"] = wikipedia_dict[wiki_rest]["chef"]

        if not flag:
            print(wiki_rest)
    
    chefs = [""]
    chefs_ids = 1
    chefs_dict[""] = {"id" : 0} #for unknown chefs
    
    for chef in wikidata_dict :
        wiki_keys = list(wikidata_dict[chef].keys())
        if not chef in chefs :
            chefs.append(chef)
            chefs_dict[chef] = {key: wikidata_dict[chef][key] for key in wiki_keys}
            chefs_dict[chef]["id"] = chefs_ids
            chefs_ids +=1

    for restaurant in restaurants_dict :
        c_chef = restaurants_dict[restaurant]["current-chef"]
        s_chef = restaurants_dict[restaurant]["starred-chef"]
        if not c_chef in chefs :
            chefs.append(c_chef)
            chefs_dict[c_chef] = {}
            chefs_dict[c_chef]["id"] = chefs_ids
            chefs_ids +=1
        if not s_chef in chefs :
            chefs.append(s_chef)
            chefs_dict[s_chef] = {}
            chefs_dict[s_chef]["id"] = chefs_ids
            chefs_ids +=1

        restaurants_dict[restaurant]["current-chef-id"] = chefs_dict[c_chef]["id"]
        restaurants_dict[restaurant]["starred-chef-id"] = chefs_dict[s_chef]["id"]

    chefs_df = pd.DataFrame(chefs_dict).transpose()
    chefs_df['id'] = chefs_df['id'].astype(int)
    chefs_df["birth-date"] = chefs_df["birth-date"].apply(lambda x: pd.to_datetime(x, format='%Y-%m-%dT%H:%M:%SZ', errors='coerce')).dt.strftime('%Y-%m-%d')
    chefs_df["death-date"] = chefs_df["death-date"].apply(lambda x: pd.to_datetime(x, format='%Y-%m-%dT%H:%M:%SZ', errors='coerce')).dt.strftime('%Y-%m-%d')
    restaurants_df = pd.DataFrame(restaurants_dict).transpose()

    return restaurants_dict, restaurants_df, chefs_dict, chefs_df


# Main function
def main():
    path_wikidata = r"wikidata_chefs/chefs.json"
    data = load_json(path_wikidata)
    dict_wikidata, df_wikidata = treat_data_wikidata(data)

    path_michelin = r"michelin_guide_webscraping/restaurant_cleaned.json"
    data = load_json(path_michelin)
    dict_michelin, df_michelin = treat_data_michelin(data)

    path_wikipedia = r'wikipedia_michelin_stars/two_three_stars_restaurant_cleaned.json'
    data = load_json(path_wikipedia)
    dict_wikipedia, df_wikipedia = treat_data_wikipedia(data)

    restaurants_dict, restaurants_df, chefs_dict, chefs_df = merging(df_wikidata, df_michelin, df_wikipedia, dict_wikidata, dict_michelin, dict_wikipedia)
    print("Saving of the restaurant table")
    restaurants_df.to_json('final_tables/restaurants_table.json', orient='index',indent=4)
    print("Saving the chef table")
    chefs_df[['id', 'birth-date', 'death-date']].to_json('final_tables/chefs_table.json', orient='index',indent=4) #à changer mais sinon c'est trop lourd, choisir un nombre limité de distinctions psq là y'en a 294


if __name__ == '__main__':
    main()
