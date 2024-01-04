Database based on the data of wikidata available from here : https://www.wikidata.org/wiki/Wikidata:Main_Page

The data can be obtained using the Query plateform provided : https://query.wikidata.org


This specific data base has been obtained using this SPARQL request :

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