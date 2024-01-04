# Wikidata SPARQL Querying Subdirectory

## Overview

This subdirectory contains the code and the data extracted from [Wikidata's SPARQL query service](https://query.wikidata.org) concerning chefs (as of January 4th, 2024).

### Contents and Usage

- **[chefs.json](chefs.json)**: json file containing the queried data

To query the data stored in the chefs.json on Wikidata's SPARQL query service, please enter the following SPARQL request :

    SELECT ?chefLabel ?countryLabel ?birthdate ?deathdate ?distinctionLabel 
    WHERE {
      {
        ?chef wdt:P106 wd:Q3499072 .
      } UNION {
        ?chef wdt:P106 wd:Q156839 .
      }
      ?chef wdt:P27 ?country .
      ?chef wdt:P569 ?birthdate .
      OPTIONAL {
        ?chef wdt:P570 ?deathdate }
      OPTIONAL {
        ?chef wdt:P166 ?distinction}
      SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en" }
    }
