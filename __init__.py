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
        self.speak(db.what_is_are_handle(message.data.get("SearchTerm")))

    @intent_handler(IntentBuilder("").require("search.example").require("SearchTerm").build())
    def handle_search_examples_intent(self, message):
        self.speak(message.data.get("SearchTerm"))
        self.speak(db.example_handle(message.data.get("SearchTerm")))

    ####################################################################################

    # TODO How Can & how often in search.mthodsHow.voc aber unterschiedliche queries???--> nur eine gemacht muss noch how often machen

    @intent_handler(IntentBuilder("").require("search.methodsHow").require("SearchTerm").build())
    def handle_how_can_intent(self, message):
        self.speak(message.data.get("SearchTerm"))
        self.speak(db.how_can_handle(message.data.get("SearchTerm")))

    # related Literature
    @intent_handler(IntentBuilder("").require("search.relatedLiterature").require("SearchTerm").build())
    def handle_related_literature_intent(self, message):
        self.speak(message.data.get("SearchTerm"))
        self.speak(db.related_literature_handle(message.data.get("SearchTerm")))

    # how many
    @intent_handler(IntentBuilder("").require("search.howMany").require("SearchTerm").build())
    def handle_how_many_intent(self, message):
        self.speak(message.data.get("SearchTerm"))
        self.speak(db.how_many_handle(message.data.get("SearchTerm")))

    #how often
    @intent_handler(IntentBuilder("").require("search.howOften").require("SearchTerm").build())
    def handle_how_often_intent(self, message):
        self.speak(message.data.get("SearchTerm"))
        self.speak(db.how_often_handle(message.data.get("SearchTerm")))


####################################################################################

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
