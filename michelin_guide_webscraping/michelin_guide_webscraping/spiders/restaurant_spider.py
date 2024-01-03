from pathlib import Path
import scrapy


# Define a Spider class that inherits from scrapy.Spider
class RestaurantSpider(scrapy.Spider):
    # Name of the Spider
    name = "restaurant"

    # Method to start requests
    def start_requests(self):
        # Generate a list of URLs for Michelin Guide pages
        urls = [f"https://guide.michelin.com/fr/fr/selection/france/restaurants/restaurants-etoiles/page/{i+1}" for i in range(32)]

        # Iterate through the URLs and yield requests with callback to 'parse' method
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    # Method to handle the response from each request
    def parse(self, response):
        # Generate a filename based on the page number
        filename = f"./michelin_guide_restaurant.html"

        # Write the response body to a file
        Path(filename).write_bytes(response.body)

        # Log a message indicating that the file has been saved
        self.log(f"Saved file {filename}")

        # Yield a dictionary with information extracted from the response
        yield {
            "restaurant-name": response.css("div[data-restaurant-name]::attr(data-restaurant-name)").getall(),
            "restaurant-region": response.css("div[data-dtm-region]::attr(data-dtm-region)").getall(),
            "restaurant-city": response.css("div[data-dtm-city]::attr(data-dtm-city)").getall(),
            "restaurant-distinction": response.css("div[data-dtm-distinction]::attr(data-dtm-distinction)").getall(),
            "restaurant-chef": response.css("div[data-dtm-chef]::attr(data-dtm-chef)").getall(),
            "restaurant-cooking-type": response.css("div[data-cooking-type]::attr(data-cooking-type)").getall(),
            "restaurant-menu-price": response.css("div[data-dtm-price]::attr(data-dtm-price)").getall()
        }