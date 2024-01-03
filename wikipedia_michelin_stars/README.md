# Wikipedia Page Webscraping Subdirectory

## Overview

This subdirectory contains the code and data extracted from [Wikipedia's list of two and three starred restaurants](https://fr.wikipedia.org/wiki/Liste_des_restaurants_deux_et_trois_étoiles_du_Guide_Michelin) (as of January 2024).

### Contents and Usage

- **[wikipedia_michelin_stars/spiders/wikipedia_spider.py](wikipedia_michelin_stars/spiders/wikipedia_spider.py)**: Code defining the Spider class (the Wikipedia web crawler) inherited from scrapy.Spider, with its parsing method.

To execute the crawling process, assuming you are in the root directory of this git:
> cd wikipedia_michelin_stars

> scrapy crawl wikipedia -O two_three_stars_restaurant_scraped.json

N.B.: The above process not only crawls the wikipedia page but also scrapes it with a good amount of preprocessing.

- **[two_three_stars_restaurant.htm](two_three_stars_restaurant.html)**: html file containing the crawled data from the wikipedia page.
- **[two_three_stars_restaurant_scraped.json](two_three_stars_restaurant_scraped.json)**: json file containing the scraped data from the html file, already proprocessed and stored in its near-to-final form.
- **[wikipedia_michelin_stars/preprocess_json.py](wikipedia_michelin_stars/preprocess_json.py)**: Code defining how the scraped data is reformatted (mostly pretty-printed in the saved json file).

To execute the formatting process of the two_three_stars_restaurant_scraped.json file, assuming you are in the root directory of this git:
> python ./wikipedia_michelin_stars/wikipedia_michelin_stars/preprocess_json.py

- **[two_three_stars_restaurant_cleaned.json](two_three_stars_restaurant_cleaned.json)**: json file containing the scraped data from the html file, formatted and pretty-printed
