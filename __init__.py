from adapt.intent import IntentBuilder
from mycroft import util
from mycroft.skills.core import MycroftSkill, intent_handler
import ocSkill.graphDBConnector as db
# import Oc.config as c

from SPARQLWrapper import SPARQLWrapper, JSON

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
        searchterm = prepare_searchterm(message.data.get("utterance"), message.data.get("SearchTerm"))
        self.speak(db.what_is_are_handle(searchterm))

    @intent_handler(IntentBuilder("").require("diff.definition").require("SearchTerm").build())
    def handle_difference_intent(self, message):
        searchterm = prepare_searchterm(message.data.get("utterance"), message.data.get("SearchTerm"))
        name1, name2 = get_names(searchterm)
        self.speak(db.difference_handle(name1, name2))

    @intent_handler(IntentBuilder("").require("usage.definition").require("SearchTerm").build())
    def handle_usage_intent(self, message):
        searchterm = prepare_searchterm(message.data.get("utterance"), message.data.get("SearchTerm"))
        self.speak(db.usage_handle(searchterm))

    @intent_handler(IntentBuilder("").require("search.example").require("SearchTerm").build())
    def handle_search_examples_intent(self, message):
        searchterm = prepare_searchterm(message.data.get("utterance"), message.data.get("SearchTerm"))
        self.speak(db.example_handle(searchterm))

    ####################################################################################

    # TODO How Can & how often in search.mthodsHow.voc aber unterschiedliche queries???--> nur eine gemacht muss noch how often machen

    @intent_handler(IntentBuilder("").require("search.methodsHow").require("SearchTerm").build())
    def handle_how_can_intent(self, message):
        searchterm = prepare_searchterm(message.data.get("utterance"), message.data.get("SearchTerm"))
        self.speak(searchterm)
        self.speak(db.how_can_handle(searchterm))

    # related Literature
    @intent_handler(IntentBuilder("").require("search.relatedLiterature").require("SearchTerm").build())
    def handle_related_literature_intent(self, message):
        searchterm = prepare_searchterm(message.data.get("utterance"), message.data.get("SearchTerm"))
        self.speak(searchterm)
        self.speak(db.related_literature_handle(searchterm))

    # how many
    @intent_handler(IntentBuilder("").require("search.howMany").require("SearchTerm").build())
    def handle_how_many_intent(self, message):
        searchterm = prepare_searchterm(message.data.get("utterance"), message.data.get("SearchTerm"))
        self.speak(searchterm)
        self.speak(db.how_many_handle(searchterm))

    # how often
    @intent_handler(IntentBuilder("").require("search.howOften").require("SearchTerm").build())
    def handle_how_often_intent(self, message):
        searchterm = prepare_searchterm(message.data.get("utterance"), message.data.get("SearchTerm"))
        self.speak(searchterm)
        answer = db.how_often_handle(searchterm)
        self.speak_dialog("counter.found", data={"name": message.data.get("SearchTerm"), "counter": answer})

    ######################
    # how does
    @intent_handler(IntentBuilder("").require("search.howDoes").require("SearchTerm").build())
    def handle_how_does_intent(self, message):
        searchterm = prepare_searchterm(message.data.get("utterance"), message.data.get("SearchTerm"))
        self.speak(searchterm)
        #self.speak(db.how_does_handle(searchterm))
        self.speak(db.how_to_step_handle(searchterm))

    # in which
    @intent_handler(IntentBuilder("").require("search.inWhich").require("SearchTerm").build())
    def handle_in_which_intent(self, message):
        searchterm = prepare_searchterm(message.data.get("utterance"), message.data.get("SearchTerm"))
        self.speak(searchterm)
        self.speak(db.in_which_handle(searchterm))

    ####################################################################################

    @intent_handler(IntentBuilder("").require("search.uses").require("SearchTerm").build())
    def handle_search_uses_intent(self, message):
        searchterm = prepare_searchterm(message.data.get("utterance"), message.data.get("SearchTerm"))
        self.speak(searchterm)
        self.speak(db.uses_handle(searchterm))


def prepare_searchterm(utterance, searchterm):
    return strip_off_ending(utterance[utterance.index(searchterm):])


def speak_no_result(self, term):
    self.speak_dialog("no.result", data={"term": term})


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
