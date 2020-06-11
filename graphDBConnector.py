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

SELECT ?entity ?score ?des ?name{
  ?search a inst:get_definition ;
      :query  "%s~" ;
      :entities ?entity .
    ?entity :score ?score .
    ?entity schema:description ?des .
    ?entity schema:name ?name
  
}
"""


def what_is_are_handle(name):
    binding = search(name, WHAT_IS_ARE_QUERY)
    if binding != "No entry":
        return binding['des']['value']
    return "No entry"


def search_fritz():
    sparql.setQuery(SEARCH_FRITZ)
    result = sparql.query().convert()
    bindings = result['results']['bindings']
    n = bindings[0]['name']['value']
    if len(n) > 0:
        return n
    return "fail"


def search(name, query):
    temp_query = query % name
    sparql.setQuery(temp_query)
    result = sparql.query().convert()
    if result:
        return check_similarity(result['results']['bindings'], name)
    return "fail"  # result['results']['bindings']


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
