# French Michelin Starred Restaurants and Chefs Database - Web Scraping and Data Querying Project

## IASD Master Program 2023/2024 - PSL Research University

### About this project

This project is the final homework assignment for the Data Acquisition, Extraction & Storage class of the IASD (Artificial Intelligence, Systems and Data) Master Program 2023/2024, at PSL Research University (Université PSL).

*The project successfully achieved the following objectives:*
- Web-scraped and compiled data from the Michelin Guide website, enriching it with Wikipedia's list of two and three-starred restaurants. 
- Extracted chef information from Wikidata's SPARQL query service to enhance the dataset with comprehensive details about chefs. 
- Integrated, normalized, and merged data from multiple sources, creating structured tables for French Michelin-starred restaurants and chefs.

## General Information

The report can be viewed in the [report.pdf](report.pdf) file. It answers to the instructions given in the [project_guidelines.pdf](project_guidelines.pdf) file provided by the professor, and the [project_description.pdf](project_description.pdf) we provided as complementary information.

The rest of the instructions can be found below. If you want to copy and recreate this project, or test it for yourself, some important information to know.

- **requirements.txt** :
Among the good practice of datascience, we encourage you to use conda or virtualenv to create python environment. 
To test your code, you are required to install the libraries of the [requirements.txt](requirements.txt) file.  
  > pip install -r requirements.txt

- **michelin_guide_webscraping** :
The [michelin_guide_webscraping](michelin_guide_webscraping) subdirectory contains the code and the data extracted from the [Michelin Guide website](https://guide.michelin.com/fr/fr) concerning French starred restaurants (as of January 3rd, 2024).
*More information about this part of the project : [michelin_guide_webscraping/README.md](michelin_guide_webscraping/README.md)*

- **wikipedia_michelin_stars** :
The [wikipedia_michelin_stars](wikipedia_michelin_stars) subdirectory contains the code and the data extracted from [Wikipedia's list of two and three starred restaurants](https://fr.wikipedia.org/wiki/Liste_des_restaurants_deux_et_trois_étoiles_du_Guide_Michelin) (as of January 3rd, 2024).
*More information about this part of the project : [wikipedia_michelin_stars/README.md](wikipedia_michelin_stars/README.md)*

- **wikidata_chefs** :
The [wikidata_chefs](wikidata_chefs) subdirectory contains the data extracted from [Wikidata's SPARQL query service](https://query.wikidata.org) concerning chefs (as of January 4th, 2024).
*More information about this part of the project : [wikidata_chefs/README.md](wikidata_chefs/README.md)*

- **final_tables** :
The [final_tables](final_tables) subdirectory contains the final database tables of the project concerning French Michelin-starred restaurants and chefs.

- **treatment.py** :
The [treatment.py](treatment.py) script integrates and normalizes chef and restaurant data from Wikidata, the Michelin Guide, and Wikipedia, creating structured tables, ultimately saving the final data tables as [final_tables/chefs_table.json](final_tables/chefs_table.json) and [final_tables/restaurants_table.json](final_tables/restaurants_table.json).

### Usage

To recreate the databases from A to Z using the code hosted on this GitHub, please :
- Install the required libraries
  > pip install -r requirements.txt
- Follow the instructions in the READMEs of the three subdirectories ([michelin_guide_webscraping/README.md](michelin_guide_webscraping/README.md), [wikipedia_michelin_stars/README.md](wikipedia_michelin_stars/README.md), [wikidata_chefs/README.md](wikidata_chefs/README.md))
- Execute the treatment.py script to concatenate, merge, and save the two tables constituting the database
  > python treatment.py

---

### Acknowledgement

This project was made possible with the guidance and support of the following :

- **Prof. Pierre Senellart**
  - Professor at *ENS Ulm, PSL*
  - Researcher in the *DI (Département d'Informatique)* at *ENS, CNRS & INRIA, UMR 8548* at *ENS Ulm, PSL* and *Université PSL*
 
This project was a group project, and was made possible thanks to the collaboration of :

- **Mathilde Kretz**, *IASD Master Program 2023/2024 student, at PSL Research University*
- **Thomas Boudras**, *IASD Master Program 2023/2024 student, at PSL Research University*
- **Alexandre Ngau**, *IASD Master Program 2023/2024 student, at PSL Research University*

### License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

---

**Note:**

This project is part of ongoing research and is subject to certain restrictions. Please refer to the license section and the [LICENSE.md](LICENSE.md) file for details on how to use this code for research purposes.
