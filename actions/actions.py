# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []





# from rasa_sdk import Action
# from rasa_sdk.events import SlotSet
# from typing import Text

# class ActionSeTone(Action):
#     def name(self) -> Text:
#         return "action_set_tone"

#     def run(self, dispatcher, tracker, domain):
#         intent = tracker.latest_message['intent']['name']
        
#         if intent == "greet_friendly":
#             return [SlotSet("tone", "friendly")]
#         elif intent == "greet_formal":
#             return [SlotSet("tone", "formal")]


from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, UserUtteranceReverted,Restarted
from rasa_sdk.executor import CollectingDispatcher

class ActionSetTone(Action):
   def name(self) -> Text:
      return "action_set_tone"

   def run(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        intent = tracker.latest_message['intent']['name']
        
        if intent == "greet_friendly":
            return [SlotSet("tone", "friendly")]
        elif intent == "greet_formal":
            return [SlotSet("tone", "formal")]
        
class ActionSetSuggestion(Action):
   def name(self) -> Text:
      return "action_set_suggestion"

   def run(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        intent = tracker.latest_message['intent']['name']
        
        suggestion= "need help?"

        return [SlotSet("suggestion", suggestion)]

class ActionHandleFallback(Action):
   def name(self) -> Text:
      return "action_handle_fallback"

   def run(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        user_message = tracker.latest_message.get("text")

        if ("elaborate" in user_message.lower()):
            return [SlotSet("msg_type", "elaborate_emotion")]
        
        emotion_keywords = ["sad", "fear", "happy", "angry", "anxious"]
        
        detected_emotion = None
        for emotion in emotion_keywords:
            if emotion in user_message.lower():
                detected_emotion = emotion
                break
                
                
        if detected_emotion:
            dispatcher.utter_message(text=f"Got it, you're feeling {detected_emotion}.")
            return [SlotSet("emotion", detected_emotion),
                    SlotSet("msg_type", "share_emotion")
                    ]
        else:
            dispatcher.utter_message(text="Sorry, I didn't understand that. Can you please clarify ")
            return [SlotSet("msg_type", "gibberish"),
                    UserUtteranceReverted()
                    ]
            
class ActionSetEmotion(Action):
   def name(self) -> Text:
      return "action_set_emotion"

   def run(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        intent = tracker.latest_message['intent']['name']
        
        
        return [SlotSet("emotion", intent),SlotSet("msg_type", "share_emotion")]
   
            
class ActionUtterWrong(Action):
   def name(self) -> Text:
      return "action_utter_wrong"

   def run(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        slots_to_keep = ["personality",]
        current_slot_values = {slot: tracker.get_slot(slot) for slot in slots_to_keep}
        kept_slots = [SlotSet(slot, value) for slot, value in current_slot_values.items()]
        
        dispatcher.utter_message(response="utter_wrong")
        return [Restarted()] + kept_slots
   

# class ActionHandleFallback(Action):
#     def name(self):
#         return "action_handle_fallback"

#     def run(self, dispatcher, tracker, domain):
#         message = tracker.latest_message.get('text')

#         # Default to out-of-scope handling
#         category = "out_of_scope"

#         if self.is_gibberish(message):
#             category = "gibberish"
#             dispatcher.utter_message("That doesn't seem to make sense. Could you clarify?")
#         elif self.contains_specific_keyword(message):
#             category = "keyword_detected"
#             dispatcher.utter_message("I noticed you mentioned something important.")

#         # Set the slot to indicate the message category
#         return [SlotSet("message_category", category), UserUtteranceReverted()]

#     def is_gibberish(self, message):
#         return all(char.isdigit() for char in message) or len(message.strip()) < 3

#     def contains_specific_keyword(self, message):
#         keywords = ["urgent", "important", "help"]
#         return any(keyword in message.lower() for keyword in keywords)




# from typing import Text, Dict, Any, List
# from rasa_sdk import Action
# from rasa_sdk.events import SlotSet

# class ActionCheckRestaurants(Action):
#    def name(self) -> Text:
#       return "action_check_restaurants"

#    def run(self,
#            dispatcher: CollectingDispatcher,
#            tracker: Tracker,
#            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#       cuisine = tracker.get_slot('cuisine')
#       q = "select * from restaurants where cuisine='{0}' limit 1".format(cuisine)
#       result = db.query(q)

#       return [SlotSet("matches", result if result is not None else [])]
