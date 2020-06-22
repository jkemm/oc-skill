# <img src="https://raw.githack.com/FortAwesome/Font-Awesome/master/svgs/solid/book.svg" card_color="#40DBB0" width="50" height="50" style="vertical-align:bottom"/> OcSkill
OC Group 2.1 (Mycroft)

## About

## Requirements
Mycroft and SPARQLWrapper (mycroft-pip install sparqlwrapper)


## Examples
* "How does the verification process work?"

## Credits
G2.1

## Category
**Information**

To Process the Input the Adapt Intent Parser was used.

To enhance the sparql queries 
we used the Lucene Connector. In addition we added a string compare if Lucene returns multiple entities with max value.

By changing the tolerance value in the graphDBConnector.py module you can change how similar the search term and the entity name have to be.
tolerance = 0 means no similarity is needed.
## Tags

##Version
This version was tested with the graphDb version of 21.06.2020

