from SPARQLWrapper import SPARQLWrapper, JSON
import difflib as diff

# import oc.config as c
tolerance = 0
action_words = ["hometown"]
detail_words = ["thal", "innsbruck"]

sparql = SPARQLWrapper('http://graphdb.sti2.at:8080/repositories/OCSS2020')
sparql.setCredentials('oc1920', 'Oc1920!')
sparql.setReturnFormat(JSON)

SEARCH_FRITZ = """
        PREFIX schema: <http://schema.org/>
            SELECT ?name 
            WHERE {
                ?person schema:name ?name .
                ?person schema:birthDate "1950-01-01" .
            }
        """

SEARCH_WHAT_IS_ARE_QUERY = """ PREFIX schema: <http://schema.org/>
            SELECT * 
            WHERE {
                ?x schema:name ?name.
                ?x schema:description ?des .
                FILTER ((contains( "%s", lcase(str(?name)))) || (contains(lcase(str(?name)), "%s")))
            }"""

SEARCH_WHAT_IS_QUERY_SIM = """ PREFIX schema: <http://schema.org/>
            SELECT * 
            WHERE {
                ?x schema:name ?name.
                ?x schema:description ?des .
            }"""

WHAT_IS_ARE_QUERY = """
PREFIX : <http://www.ontotext.com/connectors/lucene#>
PREFIX inst: <http://www.ontotext.com/connectors/lucene/instance#>
PREFIX schema: <http://schema.org/>

SELECT * {
  ?search a inst:get_definition ;
      :query  "%s~" ;
      :entities ?entity .
    ?entity :score ?score .
    ?entity schema:description ?des .
    ?entity schema:name ?name
  
}
"""

########
# Query for How Does xxx Intent, returns one result with highest score
# Example: How does semi-automatic editing supports the user?
########
HOW_DOES_QUERY = """
PREFIX : <http://www.ontotext.com/connectors/lucene#>
PREFIX inst: <http://www.ontotext.com/connectors/lucene/instance#>
PREFIX schema: <http://schema.org/>

SELECT ?entity ?des{
  ?search a inst:get_definition ;
      :query  "%s" ;
      :limit "1" ;
      :entities ?entity .
    ?entity :score ?score .
    ?entity schema:description ?des 

}
"""

########
# Query for In Which xxx Intent, returns one result with highest score
# Example: In which format is the generated annotation source presented by the semantify.it
########
IN_WHICH_QUERY = """
PREFIX : <http://www.ontotext.com/connectors/lucene#>
PREFIX inst: <http://www.ontotext.com/connectors/lucene/instance#>
PREFIX schema: <http://schema.org/>
SELECT ?entity ?des{
  ?search a inst:in_which ;
      :query  "%s" ;
      :entities ?entity ;
      :limit "1" .
    ?entity :score ?score .
    ?entity schema:describe ?des 
}
"""

########
# Query for HowToSteps, returns one result with highest score, Step Position + Step Text
# Example: How does the verification process work?
########
SEARCH_HOW_TO_STEP_QUERY = """
    PREFIX : <http://www.ontotext.com/connectors/lucene#>
    PREFIX inst: <http://www.ontotext.com/connectors/lucene/instance#>
    PREFIX schema: <http://schema.org/>

    SELECT ?position ?stepText {
      ?search a inst:get_HowToStep ;
          :query  "%s" ;
          :limit "1" ;
          :entities ?entity .
        ?entity :score ?score .
        ?entity schema:step: ?step .        
        ?step schema:position ?position .
        ?step schema:text ?stepText .
        ?entity schema:name ?name
    }
"""

#######################################################################################

########
# Query for HowMany, returns usedByNumberOfPeople 
# Example: How many households are smart speakers already introduced
########
SEARCH_HOW_MANY_QUERY = """
    PREFIX : <http://www.ontotext.com/connectors/lucene#>
    PREFIX inst: <http://www.ontotext.com/connectors/lucene/instance#>
    PREFIX schema: <http://schema.org/>
    PREFIX knowledgeGraph: <http://www.knowledgegraphbook.ai/schema/>

    SELECT * {
      ?search a inst:get_howMany ;
          :query  "%s~" ;
          :entities ?entity .
        ?entity :score ?score .
      ?entity knowledgeGraph:usedByNumberOfPeople ?counter .
      ?entity schema:name ?name 
}
"""

########
# Query for HowOften, searches name and returns userInteractionCount 
# Example: How often is Schema.org used?
########
SEARCH_HOW_OFTEN_QUERY = """
    PREFIX : <http://www.ontotext.com/connectors/lucene#>
    PREFIX inst: <http://www.ontotext.com/connectors/lucene/instance#>
    PREFIX schema: <http://schema.org/>

    SELECT * {
      ?search a inst:get_howOften ;
          :query  "%s~" ;
          :entities ?entity .
        ?entity :score ?score .
      ?entity schema:interactionStatistic ?interaction.
      ?interaction schema:userInteractionCount ?counter .
      ?entity schema:name ?name
}
"""

######## ?datePublished ?authorname
# Query for related Literature, searches name (e.g. Machine Learning, Schema.org, ...) and returns information about related article 
# Example: How often is Schema.org used?
########
SEARCH_RELATED_LITERATURE_QUERY = """
    PREFIX : <http://www.ontotext.com/connectors/lucene#>
    PREFIX inst: <http://www.ontotext.com/connectors/lucene/instance#>
    PREFIX schema: <http://schema.org/>
    PREFIX knowledge: <http://www.knowledgegraphbook.ai/schema/>

    SELECT * {
      ?search a inst:get_additionalLiterature  ;
          :query  "%s~" ;
          :entities ?entity .
        ?entity :score ?score .
        ?entity knowledge:relatedLiterature ?relatedLiterature .
        ?relatedLiterature schema:headline ?headline .
        ?relatedLiterature schema:datePublished ?datePublished .
        ?relatedLiterature schema:author ?author .
        ?author schema:name ?name .   
}
"""

########
# Query for how can, searches name and returns description --> TODO: kann man da auch die What is query verwenden? 
# Example: How often is Schema.org used?
########
SEARCH_HOW_CAN_QUERY = """
   PREFIX : <http://www.ontotext.com/connectors/lucene#>
   PREFIX inst: <http://www.ontotext.com/connectors/lucene/instance#>
   PREFIX schema: <http://schema.org/>

   SELECT * {
     ?search a inst:get_howCan ;
         :query  "%s~" ;
         :entities ?entity .
       ?entity :score ?score .
       ?entity schema:description ?des .
       ?entity schema:name ?name
}
"""

SEARCH_EXAMPLE_QUERY = """
    PREFIX : <http://www.ontotext.com/connectors/lucene#>
    PREFIX inst: <http://www.ontotext.com/connectors/lucene/instance#>
    PREFIX schema: <http://schema.org/>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    
    SELECT * {
      ?search a inst:get_example ;
          :query  "%s~" ;
          :entities ?entity .
        ?entity :score ?score .
        ?entity skos:example ?example .
        ?example schema:name ?exampleName .
        ?entity schema:name ?name
      
    }
"""


def what_is_are_handle(name):
    binding = search(name, WHAT_IS_ARE_QUERY)
    if binding != "No entry":
        return binding['des']['value']
    return "No entry"


def in_which_handle(name):
    binding = search(name, IN_WHICH_QUERY)
    if binding != "No entry":
        return binding['des']['value']
    return "No entry"


def how_does_handle(name):
    binding = search(name, HOW_DOES_QUERY)
    if binding != "No entry":
        return binding['des']['value']
    return "No entry"


def how_to_step_handle(name):
    binding = search(name, SEARCH_HOW_TO_STEP_QUERY)
    if binding != "No entry":
        return binding['stepName']['value']
    return "No entry"


#####################################
def how_many_handle(name): #is working
    binding = search(name, SEARCH_HOW_MANY_QUERY)
    if binding != "No entry":
        return binding['counter']['value']
    return "No entry"


def how_often_handle(name): #is working
    binding = search(name, SEARCH_HOW_OFTEN_QUERY)
    if binding != "No entry":
        return binding['counter']['value']
    return "No entry"


def related_literature_handle(name): #TODO kann man da auch mehrere Felder ausgeben?
    binding = search(name, SEARCH_RELATED_LITERATURE_QUERY)
    if binding != "No entry":
        return binding['headline']['value']
    return "No entry"


def how_can_handle(name): #is working
    binding = search(name, SEARCH_HOW_CAN_QUERY)
    if binding != "No entry":
        return binding['des']['value']
    return "No entry"


#####################################


def example_handle(name):
    binding = search_multiple(name, SEARCH_EXAMPLE_QUERY)
    if binding != "No entry":
        return binding
    return "No entry"


def search_fritz():
    sparql.setQuery(SEARCH_FRITZ)
    result = sparql.query().convert()
    bindings = result['results']['bindings']
    n = bindings[0]['name']['value']
    if len(n) > 0:
        return n
    return "fail"


def search_multiple(name, query):
    temp_query = query % name
    sparql.setQuery(temp_query)
    result = sparql.query().convert()
    if result:
        return check_similarity_multiple(result['results']['bindings'], name)
    return "fail"


def search(name, query):
    temp_query = query % name
    sparql.setQuery(temp_query)
    result = sparql.query().convert()
    if result:
        return check_similarity(result['results']['bindings'], name)
    return "fail"  # result['results']['bindings']


def check_similarity_multiple(bindings, name):
    sim = diff.SequenceMatcher(None, name, bindings[0]['name']['value']).ratio()
    final_result = ""
    for b in bindings:
        temp = diff.SequenceMatcher(None, name, b['name']['value']).ratio()
        if sim < temp:
            sim = temp
        elif sim == temp:
            final_result = final_result + b['exampleName']['value'] + "\n"
    if sim > tolerance:
        return str(final_result)
    return "No entry"


def check_similarity(bindings, name):
    result = bindings[0]
    sim = diff.SequenceMatcher(None, name, bindings[0]['name']['value']).ratio()
    for b in bindings:
        temp = diff.SequenceMatcher(None, name, b['name']['value']).ratio()
        if sim < temp:
            sim = temp
            result = b

    if sim > tolerance:
        return result
    return "No entry"
