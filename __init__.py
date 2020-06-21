from adapt.intent import IntentBuilder
from mycroft import util
from mycroft.skills.core import MycroftSkill, intent_handler
import ocSkill.graphDBConnector as db
import string
# import Oc.config as c

from SPARQLWrapper import SPARQLWrapper, JSON

endwords = [
    "used",
    "needed",
    "about"
]


class Oc(MycroftSkill):
    def __init__(self):
        super(Oc, self).__init__(name="Oc")
        self.lastSearchTerm = ""

    @intent_handler(IntentBuilder("").require("search.definition").require("SearchTerm").build())
    def handle_search_definition_intent(self, message):
        searchterm = prepare_searchterm(message.data.get("utterance"), message.data.get("SearchTerm"))
        result = db.what_is_are_handle(searchterm)

        if result == "No entry":
            self.speak_dialog("no.entry", data={"name": searchterm})
        else:
            self.speak(result)

    @intent_handler(IntentBuilder("").require("diff.definition").require("SearchTerm").build())
    def handle_difference_intent(self, message):
        searchterm = prepare_searchterm(message.data.get("utterance"), message.data.get("SearchTerm"))
        name1, name2 = get_names(searchterm)
        result = db.difference_handle(name1, name2)
        if result == "No entry":
            self.speak_dialog("no.entry", data={"name": searchterm})
        else:
            self.speak(result)

    @intent_handler(IntentBuilder("").require("definition.definition").require("SearchTerm").build())
    def handle_definition_intent(self, message):
        searchterm = prepare_searchterm(message.data.get("utterance"), message.data.get("SearchTerm"))
        result = db.what_is_definition_handle(searchterm)
        if result == "No entry":
            self.speak_dialog("no.entry", data={"name": searchterm})
        else:
            self.speak(result)

    @intent_handler(IntentBuilder("").require("purpose.definition").require("SearchTerm").build())
    def handle_purpose_intent(self, message):
        searchterm = prepare_searchterm(message.data.get("utterance"), message.data.get("SearchTerm"))
        result = db.what_is_purpose_handle(searchterm)
        if result == "No entry":
            self.speak_dialog("no.entry", data={"name": searchterm})
        else:
            self.speak(result)



    @intent_handler(IntentBuilder("").require("usage.definition").require("SearchTerm").build())
    def handle_usage_intent(self, message):
        searchterm = prepare_searchterm(message.data.get("utterance"), message.data.get("SearchTerm"))
        result = db.usage_handle(searchterm)
        if result == "No entry":
            self.speak_dialog("no.entry", data={"name": searchterm})
        else:
            self.speak(result)

    @intent_handler(IntentBuilder("").require("search.example").require("SearchTerm").build())
    def handle_search_examples_intent(self, message):
        searchterm = prepare_searchterm(message.data.get("utterance"), message.data.get("SearchTerm"))
        result = db.example_handle(searchterm)
        if result == "No entry":
            self.speak_dialog("no.entry", data={"name": searchterm})
        else:
            self.speak_dialog("found.example", data={"examples": result, "name": searchterm})

    ####################################################################################

    @intent_handler(IntentBuilder("").require("search.methodsHow").require("SearchTerm").build())
    def handle_how_can_intent(self, message):
        searchterm = prepare_searchterm(message.data.get("utterance"), message.data.get("SearchTerm"))
        result = db.how_can_handle(searchterm)
        if result == "No entry":
            self.speak_dialog("no.entry", data={"name": searchterm})
        else:
            self.speak(result)

    # related Literature
    @intent_handler(IntentBuilder("").require("search.relatedLiterature").require("SearchTerm").build())
    def handle_related_literature_intent(self, message):
        searchterm = prepare_searchterm(message.data.get("utterance"), message.data.get("SearchTerm"))
        binding_authors, binding_headline, binding_publisheddate = db.related_literature_handle(searchterm)
        if binding_headline == "No entry":
            self.speak_dialog("no.entry", data={"name": searchterm})
        else:
            self.speak_dialog("found.literature", data={"author": binding_authors, "headline": binding_headline,
                                                        "publishedDate": binding_publisheddate, "name": searchterm})

    # how many
    @intent_handler(IntentBuilder("").require("search.howMany").require("SearchTerm").build())
    def handle_how_many_intent(self, message):
        searchterm = prepare_searchterm(message.data.get("utterance"), message.data.get("SearchTerm"))
        result = db.how_many_handle(searchterm)
        if result == "No entry":
            self.speak_dialog("no.entry", data={"name": searchterm})
        else:
            self.speak_dialog("counter.found", data={"name": searchterm, "counter": result})

    # how often
    @intent_handler(IntentBuilder("").require("search.howOften").require("SearchTerm").build())
    def handle_how_often_intent(self, message):
        searchterm = prepare_searchterm(message.data.get("utterance"), message.data.get("SearchTerm"))
        result = db.how_often_handle(searchterm)
        if result == "No entry":
            self.speak_dialog("no.entry", data={"name": searchterm})
        else:
            self.speak_dialog("counter.found", data={"name": searchterm, "counter": result})

    ######################
    # how does
    @intent_handler(IntentBuilder("").require("search.howDoes").require("SearchTerm").build())
    def handle_how_does_intent(self, message):
        searchterm = prepare_searchterm(message.data.get("utterance"), message.data.get("SearchTerm"))
        result = db.how_to_step_handle(searchterm)
        if result == "No entry":
            self.speak_dialog("no.entry", data={"name": searchterm})
        else:
            self.speak(result)

    # in which
    @intent_handler(IntentBuilder("").require("search.inWhich").require("SearchTerm").build())
    def handle_in_which_intent(self, message):
        searchterm = prepare_searchterm(message.data.get("utterance"), message.data.get("SearchTerm"))
        result = db.in_which_handle(searchterm)
        if result == "No entry":
            self.speak_dialog("no.entry", data={"name": searchterm})
        else:
            self.speak(result)

    ####################################################################################

    @intent_handler(IntentBuilder("").require("search.uses").require("SearchTerm").build())
    def handle_search_uses_intent(self, message):
        searchterm = prepare_searchterm(message.data.get("utterance"), message.data.get("SearchTerm"))
        result = db.uses_handle(searchterm)
        if result == "No entry":
            self.speak_dialog("no.entry", data={"name": searchterm})
        else:
            self.speak(result)


def prepare_searchterm(utterance, searchterm):
    translator = str.maketrans(string.punctuation, ' '*len(string.punctuation))
    utterance = utterance.lower()
    searchterm = searchterm.lower()
    term = strip_off_ending(utterance[utterance.index(searchterm):])
    return term.translate(translator)


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
