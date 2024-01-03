import json


def preprocess_data(input_path, output_path):
    # Read data from the input JSON file
    with open(input_path, 'r') as json_file:
        data_dict = json.load(json_file)

    # Store only the part of the input json to save and pretty print
    preprocessed_dict = data_dict[0]["restaurants"]

    # Write the preprocessed data to a new JSON file
    with open(output_path, "w") as json_file:
        json.dump(preprocessed_dict, json_file, indent=4)

    # Print a message indicating that the file has been saved
    print(f"Preprocessed data saved to: {output_path}")


if __name__ == "__main__":
    # Define input and output file paths
    input_file_path = './wikipedia_michelin_stars/two_three_stars_restaurant_scraped.json'
    output_file_path = './wikipedia_michelin_stars/two_three_stars_restaurant_cleaned.json'

    # Call the preprocess_data function
    preprocess_data(input_file_path, output_file_path)
