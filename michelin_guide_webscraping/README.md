# Michelin Guide Webscraping Subdirectory

## Overview

This subdirectory contains the code and data extracted from the [Michelin Guide website](https://guide.michelin.com/fr/fr) concerning French starred restaurants (as of January 2024).

### Contents and Usage

- **[michelin_guide_webscraping/spiders/restaurant_spider.py](michelin_guide_webscraping/spiders/restaurant_spider.py)**: Code defining the Spider class (the Michelin Guide web crawler) inherited from scrapy.Spider, with its parsing method.

To execute the crawling process, assuming you are in the root directory of this git:
> cd michelin_guide_webscraping

> scrapy crawl restaurant -O restaurant_scraped.json

- **[michelin_guide_webscraping/restaurant-page.htm](michelin_guide_webscraping/restaurant-page.html)**: html file containing the crawled data from the website
- **[restaurant_scraped.json](restaurant_scraped.json)**: json file containing the scraped data from the html file
- **[michelin_guide_webscraping/preprocess_json.py](michelin_guide_webscraping/preprocess_json.py)**: Code defining how the scraped data in the json file formed from the parsing method of the spider is reorganized and stored.

To execute the formatting process of the restaurant_scraped.json file, assuming you are in the root directory of this git:
> python ./michelin_guide_webscraping/michelin_guide_webscraping/preprocess_json.py

- **[restaurant_cleaned.json](restaurant_cleaned.json)**: json file containing the scraped data from the html file, formatted
