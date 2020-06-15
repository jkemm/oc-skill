from adapt.intent import IntentBuilder
from mycroft import util
from mycroft.skills.core import MycroftSkill, intent_handler
import ocSkill.graphDBConnector as db
# import Oc.config as c

from SPARQLWrapper import SPARQLWrapper, JSON

fillwords = [
    'of a',
    'of an',
    'the',
    'for',
    'a',
    'an',
    'of',
    'about'
]

endwords = [
    "used",
    "needed"
]


class Oc(MycroftSkill):
    def __init__(self):
        super(Oc, self).__init__(name="Oc")
        self.lastSearchTerm = ""

    @intent_handler(IntentBuilder("").require("search.definition").require("SearchTerm").build())
    def handle_search_definition_intent(self, message):
        self.speak(message.data.get("SearchTerm"))
        self.speak(db.what_is_are_handle(message.data.get("SearchTerm")))

    @intent_handler(IntentBuilder("").require("diff.definition").require("SearchTerm").build())
    def handle_difference_intent(self, message):
        name1, name2 = get_names(message.data.get("SearchTerm"))
        self.speak(name1 + " " + name2)
        self.speak(db.difference_handle(name1, name2))

    @intent_handler(IntentBuilder("").require("usage.definition").require("SearchTerm").build())
    def handle_usage_intent(self, message):
        searchterm = strip_off_ending(message.data.get("SearchTerm"))
        self.speak(searchterm)
        self.speak(db.usage_handle(searchterm))


def speak_no_result(self, term):
    self.speak_dialog("no.result", data={"term": term})


def normalize_search_term(search_term):
    search_term = search_term.strip()
    for word in fillwords:
        if search_term.startswith(word + ' '):
            search_term = search_term.replace(word + ' ', '', 1)

    for word in endwords:
        if search_term.endswith(word):
            search_term += word

    return search_term


def strip_off_ending(searchterm):
    searchterm = searchterm.strip()
    for word in endwords:
        if searchterm.endswith(word):
            return str(searchterm.rsplit(' ', 1)[0])
    return searchterm


def get_names(msg):
    names = msg.split("and")
    return names[0], names[1]


def create_skill():
    return Oc()
