import requests
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, UserUtteranceReverted,Restarted,SessionStarted,ActionExecuted
from rasa_sdk.executor import CollectingDispatcher


      
class ActionSessionStart(Action):
    def name(self):
        return "action_session_start"

    def run(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_id = tracker.sender_id
        api_url = f"http://localhost:8000/api/get_initial/"

        personality, preference =None, "new", 

        try:
            response = requests.post(api_url, json={"user_id": user_id}, timeout=5)
            if response.status_code == 200:
                data = response.json()
                personality = data.get("personality", "new")
                preference = data.get("preference", None)

        except requests.exceptions.RequestException:
            dispatcher.utter_message("I couldn't fetch your profile. We'll proceed with default settings.")

        # Set slots before the conversation starts
        return [
            SessionStarted(),
            SlotSet("personality", personality),
            SlotSet("preference", preference),
            ActionExecuted("action_listen"), 
        ]
      
class ActionSetSuggestion(Action):
   def name(self) -> Text:
      return "action_set_suggestion"

   def run(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        intent = tracker.latest_message['intent']['name']
        
        suggestion= "SUGGESTION"
        help= "HELP"

        return [SlotSet("suggestion", suggestion),
                SlotSet("help", help)
                ]

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


