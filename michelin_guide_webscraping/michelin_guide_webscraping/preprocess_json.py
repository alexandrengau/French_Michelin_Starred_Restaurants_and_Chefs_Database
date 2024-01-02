import json


def preprocess_data(input_path, output_path):
    # Read data from the input JSON file
    with open(input_path, 'r') as json_file:
        data_dict = json.load(json_file)

    # Initialize an empty list to store preprocessed data
    preprocessed_dict = []

    # Iterate through the data and restructure it
    for row in range(len(data_dict)):
        for element in range(len(data_dict[row]["restaurant-name"])):
            preprocessed_dict.append({
                "restaurant-name": data_dict[row]["restaurant-name"][element],
                "restaurant-region": data_dict[row]["restaurant-region"][element],
                "restaurant-city": data_dict[row]["restaurant-city"][element],
                "restaurant-distinction": data_dict[row]["restaurant-distinction"][element],
                "restaurant-chef": data_dict[row]["restaurant-chef"][element],
                "restaurant-cooking-type": data_dict[row]["restaurant-cooking-type"][element],
                "restaurant-menu-price": data_dict[row]["restaurant-menu-price"][element]
            })

    # Write the preprocessed data to a new JSON file
    with open(output_path, "w") as json_file:
        json.dump(preprocessed_dict, json_file, indent=4)

    # Print a message indicating that the file has been saved
    print(f"Preprocessed data saved to: {output_path}")

if __name__ == "__main__":
    # Define input and output file paths
    input_file_path = './michelin_guide_webscraping/restaurant_scraped.json'
    output_file_path = './michelin_guide_webscraping/restaurant_cleaned.json'

    # Call the preprocess_data function
    preprocess_data(input_file_path, output_file_path)
