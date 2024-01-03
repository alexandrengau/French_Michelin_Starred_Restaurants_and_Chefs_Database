from pathlib import Path
import scrapy


# Define a Spider class that inherits from scrapy.Spider
class WikipediaSpider(scrapy.Spider):
    # Name of the Spider
    name = "wikipedia"

    def start_requests(self):
        url = "https://fr.wikipedia.org/wiki/Liste_des_restaurants_deux_et_trois_étoiles_du_Guide_Michelin"
        yield scrapy.Request(url=url, callback=self.parse)

    # Method to handle the response from each request
    def parse(self, response):
        filename = f"./two_three_stars_restaurant.html"
        Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")

        # List of regions to exclude
        excluded_regions = [
            "Allemagne", "Italie", "Espagne", "Royaume-Uni",
            "Pays-Bas", "Belgique", "Suisse", "Autriche",
            "Danemark", "Norvège", "Suède"
        ]

        restaurants = []

        # Assuming the relevant data is in a table, adjust the selector accordingly
        rows = response.css('table.wikitable tbody tr')

        for row in rows:
            name = row.css('td:nth-child(3) i::text').get()
            name_i = row.css('td:nth-child(3) i a::text').get()

            # Concatenate name and name_it, handling null values
            restaurant_name = name + (' ' + name_i if name_i else '') if name else name_i

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

            if len(restaurants) >= 29:
                break

        # Find the tables after the specified text
        table_selector = response.xpath('//p[i[contains(text(), "Liste des 75 restaurants deux étoiles du Guide '
                                        'Michelin 2023")]]/following-sibling::table[@class="wikitable sortable"]')

        # Extract the table HTML
        table_html = table_selector.extract_first()

        restaurants_2 = []

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

            if len(restaurants_2) >= 75:
                break

        yield {'restaurants': restaurants+restaurants_2}
