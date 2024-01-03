from pathlib import Path
import scrapy


# Define a Spider class that inherits from scrapy.Spider
class WikipediaSpider(scrapy.Spider):
    # Name of the Spider
    name = "wikipedia"

    def start_requests(self):
        # Starting URL for the Spider
        url = "https://fr.wikipedia.org/wiki/Liste_des_restaurants_deux_et_trois_étoiles_du_Guide_Michelin"
        # Make a request to the URL, and when the response is received, call the parse method
        yield scrapy.Request(url=url, callback=self.parse)

    # Method to handle the response from each request
    def parse(self, response):
        # Save the HTML content of the response to a file for inspection
        filename = f"./two_three_stars_restaurant.html"
        Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")

        # List of regions to exclude (will be used throughout the parsing)
        excluded_regions = [
            "Allemagne", "Italie", "Espagne", "Royaume-Uni",
            "Pays-Bas", "Belgique", "Suisse", "Autriche",
            "Danemark", "Norvège", "Suède"
        ]

        ### THREE STAR RESTAURANTS ###

        # List to store 3-star restaurants
        restaurants = []

        # Assuming the relevant data is in a table
        rows = response.css('table.wikitable tbody tr')

        for row in rows:
            name = row.css('td:nth-child(3) i::text').get()
            name_i = row.css('td:nth-child(3) i a::text').get()

            # Concatenate name and name_it, handling null values
            restaurant_name = name + (' ' + name_i if name_i else '') if name else name_i

            # Dictionary to store restaurant details
            restaurant = {
                'restaurant-name': restaurant_name,
                'restaurant-region': row.css('td:nth-child(6) a::text').get(),
                'restaurant-city': row.css('td:nth-child(4) a::text').get(),
                "restaurant-distinction": "3 star",
                'restaurant-chef': row.css('td:nth-child(2) a::text').get(),
            }

            # Check if the city is not None and the region is not in the excluded list
            if restaurant['restaurant-city'] is not None and restaurant['restaurant-region'] not in excluded_regions:
                restaurants.append(restaurant)

            # Break the loop after collecting 29 restaurants
            # ==> Wikipedia says there are 29 3-star restaurants in France and Monaco
            # at the date the website was looked up (January 3rd, 2024)
            if len(restaurants) >= 29:
                break

        ### TWO STAR RESTAURANTS ###

        # Find the tables after the specified text
        table_selector = response.xpath('//p[i[contains(text(), "Liste des 75 restaurants deux étoiles du Guide '
                                        'Michelin 2023")]]/following-sibling::table[@class="wikitable sortable"]')

        # Extract the table HTML
        table_html = table_selector.extract_first()

        # List to store 2-star restaurants
        restaurants_2 = []

        # Create a new scrapy Selector from the extracted HTML
        rows = scrapy.Selector(text=table_html).css('tbody tr')

        for row in rows:
            name = row.css('td:nth-child(2) i::text').get()
            name_i = row.css('td:nth-child(2) i a::text').get()
            name_td = row.css('td:nth-child(2)::text').get()

            # Concatenate name and name_i, handling null values
            restaurant_name = ' '.join(filter(None, [name, name_i]))
            # If restaurant_name is still empty, use name_td
            restaurant_name = restaurant_name if restaurant_name else name_td

            chef = row.css('td:nth-child(1) a::text').get()
            chef_td = row.css('td:nth-child(1)::text').get()
            # Concatenate chef and name_i, handling null values
            chef_name = chef + (' ' + chef_td if chef_td else '') if chef else chef_td

            # Dictionary to store restaurant details
            restaurant_2 = {
                'restaurant-name': restaurant_name,
                'restaurant-region': row.css('td:nth-child(5) a::text').get(),
                'restaurant-city': row.css('td:nth-child(3) a::text').get(),
                "restaurant-distinction": "2 star",
                'restaurant-chef': chef_name,
            }

            # Check if the city is not None and the region is not in the excluded list
            if restaurant_2['restaurant-city'] is not None and restaurant_2['restaurant-region'] not in excluded_regions:
                restaurants_2.append(restaurant_2)

            # Break the loop after collecting 75 restaurants
            # ==> Wikipedia says there are 75 2-star restaurants in France and Monaco
            # at the date the website was looked up (January 3rd, 2024)
            if len(restaurants_2) >= 75:
                break

        # Yield the final result as a dictionary with a list of restaurants
        yield {'restaurants': restaurants + restaurants_2}
