# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

#
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import (
    SlotSet,
    UserUtteranceReverted,
    ConversationPaused,
    EventType,
)

#
#
USER_INTENT_OUT_OF_SCOPE = "out_of_scope"

class ActionGreetUser(Action):
    """Greets the user with/without privacy policy"""
    print("Inside ActionGreetUser")

    def name(self) -> Text:
        print("Inside ActionGreetUser name")
        return "action_greet_user"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[EventType]:
        print("Inside ActionGreetUser run")
        intent = tracker.latest_message["intent"].get("name")
        print("intent",intent)
        shown_privacy = tracker.get_slot("shown_privacy")
        print("shown_privacy",shown_privacy)
        name_entity = next(tracker.get_latest_entity_values("name"), None)
        print("name_entity",name_entity)
        if intent == "greet" or intent == "mood_great" or (intent == "enter_data" and name_entity):
            if shown_privacy and name_entity and name_entity.lower() != "sara":
                dispatcher.utter_message(response="utter_greet_name", name=name_entity)
                return []
            else:
                dispatcher.utter_message(response="utter_inform_privacypolicy")
                return [SlotSet("shown_privacy", True)]
        return []
