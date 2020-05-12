from mycroft import MycroftSkill, intent_file_handler


class Oc(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('oc.intent')
    def handle_oc(self, message):
        self.speak_dialog('oc')


def create_skill():
    return Oc()

