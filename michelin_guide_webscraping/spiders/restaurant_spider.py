from pathlib import Path
import scrapy


class RestaurantSpider(scrapy.Spider):
    name = "restaurant"

    def start_requests(self):
        urls=[]
        for i in range(32):
            urls.append(f"https://guide.michelin.com/fr/fr/selection/france/restaurants/restaurants-etoiles/page/{i+1}")
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # page = response.url.split("/")[-2]
        # filename = f"./michelin_guide_webscraping/restaurant-{page}.html"
        # Path(filename).write_bytes(response.body)
        # self.log(f"Saved file {filename}")
        yield {"restaurant-name": response.css("div[data-restaurant-name]::attr(data-restaurant-name)").getall(),
               "restaurant-region": response.css("div[data-dtm-region]::attr(data-dtm-region)").getall(),
               "restaurant-city": response.css("div[data-dtm-city]::attr(data-dtm-city)").getall(),
               "restaurant-distinction": response.css("div[data-dtm-distinction]::attr(data-dtm-distinction)").getall(),
               "restaurant-chef": response.css("div[data-dtm-chef]::attr(data-dtm-chef)").getall(),
               "restaurant-cooking-type": response.css("div[data-cooking-type]::attr(data-cooking-type)").getall(),
               "restaurant-menu-price": response.css("div[data-dtm-price]::attr(data-dtm-price)").getall()}
