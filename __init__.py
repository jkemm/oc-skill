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
    '.org',
    '.com',
    '.at'
]


class Oc(MycroftSkill):
    def __init__(self):
        super(Oc, self).__init__(name="Oc")
        self.lastSearchTerm = ""

    @intent_handler(IntentBuilder("").require("search.definition").require("SearchTerm").build())
    def handle_search_definition_intent(self, message):
        self.speak(message.data.get("SearchTerm"))
        if message.data.get("SearchTerm") == "person":
            self.speak(db.search_fritz())
        else:
            self.speak(db.what_is_are_handle(message.data.get("SearchTerm")))


def speak_no_result(self, term):
    self.speak_dialog("no.result", data={"term": term})


def normalize_search_term(search_term, utterance):
    search_term = search_term.strip()
    for word in c.fillwords:
        if search_term.startswith(word + ' '):
            search_term = search_term.replace(word + ' ', '', 1)

    for word in c.endwords:
        if utterance.endswith(word):
            search_term += word

    return search_term


def create_skill():
    return Oc()
