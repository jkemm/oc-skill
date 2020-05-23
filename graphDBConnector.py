from SPARQLWrapper import SPARQLWrapper, JSON
import difflib as diff

# import oc.config as c

action_words = ["hometown"]
detail_words = ["thal", "innsbruck"]

sparql = SPARQLWrapper('http://graphdb.sti2.at:8080/repositories/kgbook')
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


def what_is_are_handle(name):
    bindings = search(name, SEARCH_WHAT_IS_ARE_QUERY)
    if len(bindings) > 0:
        return bindings[0]['des']['value']
    return "No entry"


def what_is_sim_handle(name):
    bindings = search2(name, SEARCH_WHAT_IS_QUERY_SIM)
    sim = diff.SequenceMatcher(None, name, bindings[0]['name']['value']).ratio()
    result = bindings[0]

    for b in bindings:
        temp = diff.SequenceMatcher(None, name, b['name']['value']).ratio()
        if sim < temp:
            sim = temp
            result = b

    if sim > 0.9:
        return result['des']['value']
    return "Nothing similar found"


def search_fritz():
    sparql.setQuery(SEARCH_FRITZ)
    result = sparql.query().convert()
    bindings = result['results']['bindings']
    n = bindings[0]['name']['value']
    if len(n) > 0:
        return n
    return "fail"


def search(name, query):
    temp_query = query % (name, name)
    sparql.setQuery(temp_query)
    result = sparql.query().convert()
    if result:
        return result['results']['bindings']
    return "fail"  # result['results']['bindings']


def search2(name, query):
    temp_query = query
    sparql.setQuery(temp_query)
    result = sparql.query().convert()
    if result:
        return result['results']['bindings']
    return "fail"  # result['results']['bindings']
