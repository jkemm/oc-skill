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
PREFIX kgbr: <http://www.knowledgegraphbook.ai/schema/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT * {
  ?search a inst:get_definition ;
      :query  "%s~" ;
      :entities ?entity .
    ?entity :score ?score .
     ?entity schema:description  ?des .
    ?entity schema:name ?name
  
}ORDER BY DESC(?score)
"""
WHAT_IS_PURPOSE = """
PREFIX : <http://www.ontotext.com/connectors/lucene#>
PREFIX inst: <http://www.ontotext.com/connectors/lucene/instance#>
PREFIX schema: <http://schema.org/>
PREFIX kgbr: <http://www.knowledgegraphbook.ai/schema/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT * {
  ?search a inst:get_definition ;
      :query  "%s~" ;
      :entities ?entity .
    ?entity :score ?score .
     ?entity  kgbr:purpose ?purpose.
    ?entity schema:name ?name
  
}ORDER BY DESC(?score)
"""

WHAT_IS_DEFINITION = """
PREFIX : <http://www.ontotext.com/connectors/lucene#>
PREFIX inst: <http://www.ontotext.com/connectors/lucene/instance#>
PREFIX schema: <http://schema.org/>
PREFIX kgbr: <http://www.knowledgegraphbook.ai/schema/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT * {
  ?search a inst:get_definition ;
      :query  "%s~" ;
      :entities ?entity .
    ?entity :score ?score .
     ?entity skos:definition ?def .
    ?entity schema:name ?name
  
}ORDER BY DESC(?score)
"""

WHAT_IS_DIFFERENCE_QUERY = """
PREFIX : <http://www.ontotext.com/connectors/lucene#>
PREFIX inst: <http://www.ontotext.com/connectors/lucene/instance#>
PREFIX schema: <http://schema.org/>
PREFIX kgbr: <http://www.knowledgegraphbook.ai/schema/>
SELECT ?entity ?score ?name ?des{
  ?search a inst:get_difference ;
      :query  "%s" ;
      :entities ?entity .
    ?entity :score ?score .
    ?entity schema:description | kgbr:purpose ?des .
    ?entity schema:name ?name
}ORDER BY DESC(?score)
"""

KEY_CHARACTERISTICS_QUERY = """
PREFIX : <http://www.ontotext.com/connectors/lucene#>
PREFIX inst: <http://www.ontotext.com/connectors/lucene/instance#>
PREFIX schema: <http://schema.org/>
PREFIX kgbr: <http://www.knowledgegraphbook.ai/schema/>

SELECT * {
  ?search a inst:get_example  ;
      :query  "%s~" ;
      :entities ?entity .
    ?entity :score ?score .
    ?entity schema:name ?name .
    ?entity <http://www.knowledgegraphbook.ai/schema/keyCharacteristic> ?characterisitcs
}
"""
USES_QUERY = """
    PREFIX : <http://www.ontotext.com/connectors/lucene#>
    PREFIX inst: <http://www.ontotext.com/connectors/lucene/instance#>
    PREFIX schema: <http://schema.org/>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    
    SELECT * {
      ?search a inst:get_use ;
          :query  "%s~" ;
          :entities ?entity .
        ?entity :score ?score .
        ?entity  <http://www.knowledgegraphbook.ai/schema/uses> ?test .
        ?entity schema:name ?name .
    	?test schema:name ?usesName
    }ORDER BY DESC(?score)
"""
########
# Query for How Does xxx Intent, returns one result with highest score
# Example: How does semi-automatic editing supports the user?
########
HOW_DOES_QUERY = """
PREFIX : <http://www.ontotext.com/connectors/lucene#>
PREFIX inst: <http://www.ontotext.com/connectors/lucene/instance#>
PREFIX schema: <http://schema.org/>

SELECT ?entity ?des ?name{
  ?search a inst:how_does ;
      :query  "%s" ;
      :limit "1" ;
      :entities ?entity .
    ?entity :score ?score .
    ?entity schema:description ?des .
    ?entity schema:name ?name

}ORDER BY DESC(?score)
"""

WHAT_IS_USAGE_QUERY = """
PREFIX : <http://www.ontotext.com/connectors/lucene#>
PREFIX inst: <http://www.ontotext.com/connectors/lucene/instance#>
PREFIX schema: <http://schema.org/>

SELECT ?entity ?score ?des ?name{
  ?search a inst:get_usage ;
      :query  "%s" ;
      :entities ?entity .
    ?entity :score ?score .
    ?entity schema:description ?des .
    ?entity schema:name ?name
  
}ORDER BY DESC(?score)
"""

########
# Query for In Which xxx Intent, returns one result with highest score
# Example: In which format is the generated annotation source presented by the semantify.it
########        
IN_WHICH_QUERY = """
PREFIX : <http://www.ontotext.com/connectors/lucene#>
PREFIX inst: <http://www.ontotext.com/connectors/lucene/instance#>
PREFIX schema: <http://schema.org/>
SELECT ?entity ?des ?name {
  ?search a inst:in_which ;
      :query  "%s" ;
      :entities ?entity ;
      :limit "1" .
    ?entity :score ?score .
    ?entity schema:describe ?des .
    ?entity schema:alternateName ?name
}ORDER BY DESC(?score)
"""

########
# Query for HowToSteps, returns one result with highest score, Step Position + Step Text
# Example: How does the verification process work?
########
SEARCH_HOW_TO_STEP_QUERY = """
    PREFIX : <http://www.ontotext.com/connectors/lucene#>
    PREFIX inst: <http://www.ontotext.com/connectors/lucene/instance#>
    PREFIX schema: <http://schema.org/>

    SELECT ?position ?stepText ?name {
      ?search a inst:get_HowToStep ;
          :query  "%s" ;
          :limit "1" ;
          :entities ?entity .
        ?entity :score ?score .
        ?entity schema:step: ?step .        
        ?step schema:position ?position .
        ?step schema:text ?stepText .
        ?entity schema:name ?name
    }ORDER BY DESC(?score)
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
}ORDER BY DESC(?score)
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
}ORDER BY DESC(?score)
"""

########
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
        ?relatedLiterature schema:headline ?name .
        ?relatedLiterature schema:datePublished ?datePublished .
        ?relatedLiterature schema:author ?author .
        ?author schema:name ?authorname .   
}ORDER BY DESC(?score)
"""

########
# Query for how can, searches name and returns description
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
}ORDER BY DESC(?score)
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
      
    }ORDER BY DESC(?score)
"""


def what_is_are_handle(name):
    binding = search(name, WHAT_IS_ARE_QUERY)
    if binding != "No entry":
        return binding['des']['value']
    return "No entry"


def what_is_purpose_handle(name):
    binding = search(name, WHAT_IS_PURPOSE)
    if binding != "No entry":
        return binding['purpose']['value']
    return "No entry"

def keyCharacteristics_handle(name):
    binding = search_multiple(name, KEY_CHARACTERISTICS_QUERY, "characterisitcs")
    if binding != "No entry":
        return binding
    return "No entry"

def what_is_definition_handle(name):
    binding = search(name, WHAT_IS_DEFINITION)
    if binding != "No entry":
        return binding['def']['value']
    return "No entry"


def difference_handle(name1, name2):
    combined_name = "name1:" + name1 + " name2:" + name2
    binding = search(combined_name, WHAT_IS_DIFFERENCE_QUERY)
    if binding != "No entry":
        return binding['des']['value']
    return "No entry"


def usage_handle(name):
    binding = search(name, WHAT_IS_USAGE_QUERY)
    if binding != "No entry":
        return binding['des']['value']


def in_which_handle(name):
    binding = search(name, IN_WHICH_QUERY)
    if binding != "No entry":
        all_binding = binding['name']['value'] + ", " + binding['des']['value']
        return all_binding
    return "No entry"


def uses_handle(name):
    binding = search(name, USES_QUERY)
    if binding != "No entry":
        return binding['usesName']['value']
    return "No entry"


# def how_does_handle(name):         # integrated into how_to_step_handle
#    binding = search(name, HOW_DOES_QUERY)
#    if binding != "No entry":
#        return binding['des']['value']
#    return "No entry"


def how_to_step_handle(name):
    bindingSteps = search(name, SEARCH_HOW_TO_STEP_QUERY)  # get howtosteps            -> position stepText
    binding = search(name, HOW_DOES_QUERY)  # Get how does description  -> des
    if bindingSteps != "No entry":
        all_binding = binding['des']['value'] + "\n\n Additonally I have the HowToSteps: " + bindingSteps['position'][
            'value'] + ". " + bindingSteps['stepText']['value']
        return all_binding

    if binding != "No entry":
        return binding['des']['value']
    return "No entry"


#####################################
def how_many_handle(name):
    binding = search(name, SEARCH_HOW_MANY_QUERY)
    if binding != "No entry":
        return binding['counter']['value']
    return "No entry"


def how_often_handle(name):
    binding = search(name, SEARCH_HOW_OFTEN_QUERY)
    if binding != "No entry":
        return binding['counter']['value']
    return "No entry"


def related_literature_handle(name):
    binding_authors = search_multiple(name, SEARCH_RELATED_LITERATURE_QUERY, "authorname")
    binding = search(name, SEARCH_RELATED_LITERATURE_QUERY)
    if binding != "No entry":
        binding_headline = binding['name']['value']
        binding_publisheddate = binding['datePublished']['value']
        return binding_authors, binding_headline, binding_publisheddate
    else:
        return None, "No entry", None


def how_can_handle(name):
    binding = search(name, SEARCH_HOW_CAN_QUERY)
    if binding != "No entry":
        return binding['des']['value']
    return "No entry"


#####################################


def example_handle(name):
    binding = search_multiple(name, SEARCH_EXAMPLE_QUERY, "exampleName")
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


def search_multiple(name, query, sqlname):
    temp_query = query % name
    sparql.setQuery(temp_query)
    result = sparql.query().convert()
    if result:
        return check_similarity_multiple(result['results']['bindings'], name, sqlname)
    return "fail"


def search(name, query):
    temp_query = query % name
    sparql.setQuery(temp_query)
    result = sparql.query().convert()
    if result:
        return check_similarity(result['results']['bindings'], name)
    return "fail"  # result['results']['bindings']


def check_similarity_multiple(bindings, name, sqlname):
    final_result = ""
    if len(bindings) <= 0:
        return "No entry"
    sim = diff.SequenceMatcher(None, name, bindings[0]['name']['value']).ratio()
    for b in bindings:
        temp = diff.SequenceMatcher(None, name, b['name']['value']).ratio()
        if sim < temp:
            sim = temp
        elif sim == temp:
            final_result = final_result + b[sqlname]['value'] + "\n"
    if sim > tolerance:
        return str(final_result)
    return "No entry"



def check_similarity(bindings, name):
    if len(bindings) <= 0:
        return "No entry"
    elif len(bindings) < 2:
        return bindings[0]

    result = bindings[0]

    sim = diff.SequenceMatcher(None, name, bindings[0]['name']['value']).ratio()

    for b in bindings:
        if float(b['score']['value']) < float(result['score']['value']):
            break

        temp = diff.SequenceMatcher(None, name, b['name']['value']).ratio()
        if sim < temp:
            sim = temp
            result = b

    return result
