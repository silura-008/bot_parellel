import requests
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, UserUtteranceReverted,Restarted,SessionStarted,ActionExecuted
from rasa_sdk.executor import CollectingDispatcher

import random

      
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
                help_line = data.get("helpline",988)
                print(data)
        except requests.exceptions.RequestException:
            print("I couldn't fetch your profile. We'll proceed with default settings.")
            personality ="new"
            preference = None
            help_line =988

        # Set slots before the conversation starts
        return [
            SessionStarted(),
            SlotSet("personality", personality),
            SlotSet("preference", preference),
            SlotSet("help_line", help_line),
            ActionExecuted("action_listen"), 
        ]

def coping_mechanism(emotion,preference,intent):
   cope_dump = {
   "Text-based":{
      "a simple breathing technique":{
         "sad" : [
            
               "I really appreciate you taking a moment for yourself. Deep Belly Breathing can bring comfort when emotions feel heavy. It helps slow down overwhelming thoughts and brings a sense of ease. Place one hand on your belly and the other on your chest. Inhale deeply through your nose for 4 seconds, letting your belly rise while your chest stays still. Hold it gently… then exhale slowly through your mouth for 6 seconds, feeling the tension release. Let's take a few breaths together and let each one bring a little more calm.",

               "It's good that you're allowing yourself this moment. Let's try Sighing Breath—it's simple but powerful. When sadness builds up, it can feel like being weighed down. This technique helps release that weight. Take a deep inhale through your nose, filling your lungs. Now exhale through your mouth with a long, audible sigh, as if letting go of the heaviness. Let's do a few more and release what no longer serves you.",

               "I appreciate you for doing this. Let's try 5-5-5 Breathing. This steady rhythm creates a sense of control and stability when sadness feels overwhelming. Inhale deeply for 5 seconds, hold for 5, and exhale slowly for 5. Let's breathe together and let each cycle bring more peace.",
            
         ],

         "anxious" : [
            
               "It's great that you're open to this. Let's try 4-7-8 Breathing—it's a simple way to slow things down. When anxiety speeds up the heart and thoughts, this method helps activate the body's natural relaxation response. Breathe in through your nose for 4 seconds, filling your lungs. Hold for 7 seconds, letting your body settle. Now exhale through your mouth for 8 seconds, as if gently blowing out a candle. Let's do this a few times and feel the tension ease with each breath.",

               "That's a good call. Alternate Nostril Breathing helps restore balance when the mind feels scattered. It harmonizes the nervous system, bringing a sense of stability and focus. Close your right nostril with your thumb and inhale deeply through your left nostril. Now, close your left nostril with your ring finger, release your thumb, and exhale through your right nostril. Inhale through your right, switch, and exhale through your left. Let's take it slow and steady.",

               "I appreciate you taking this step. Let's try Ocean Breath. The gentle 'haaa' sound created during exhalation naturally calms the nervous system, like listening to ocean waves. Inhale deeply through your nose, and as you exhale through your mouth, make a soft 'haaa' sound. If it feels good, close your mouth and exhale through your nose while making the same soft sound in your throat. Let's try it together and let the waves of breath wash away stress.",

               "It's strong of you to do this. Let's try Feather Breathing. When anxiety takes over, controlled slow exhalation signals safety to the body. Imagine you're holding a delicate feather in front of you. Inhale deeply through your nose, and then exhale slowly through pursed lips, as if trying to make the feather float without blowing it away. This kind of slow, controlled breath helps the nervous system shift into a calmer state."
            
         ],

         "anger" :[
            
               "I admire you for taking a moment to cool down. Let's try Cooling Breath—it's refreshing and helps ease frustration. Anger builds heat in the body, and this technique naturally cools and soothes. Curl your tongue into a tube shape (or purse your lips if that's easier). Inhale deeply through your mouth, like sipping through a straw, feeling the cool air. Now close your mouth and exhale slowly through your nose. With each breath, imagine the heat of the moment fading away.",

               "It's good that you're letting yourself release this tension. Let's try Lion's Breath—a powerful way to let go. Anger carries a lot of energy, and this technique provides a controlled release. Take a deep breath in through your nose, filling your lungs. Now, open your mouth wide, stick out your tongue, and exhale forcefully with a strong 'haaa' sound. Try a few rounds and notice how your body feels as you let the tension go.",

               "Great!, Let's do Woodchopper Breath—it's great for physically releasing pent-up energy. Anger sometimes needs movement to dissipate, and this technique mimics that. Stand or sit up tall. Inhale deeply through your nose, raising your arms above your head. Then, as you exhale with a strong 'haaa' sound, swing your arms down as if chopping wood. Let's do this a few times and let go of what's weighing you down.",

               "I appreciate you trying this. Let's do Volcano Breath. This technique channels frustration into a movement that feels expressive yet calming. Place your hands together at your chest. As you inhale deeply through your nose, raise your arms up like lava rising in a volcano. Then exhale strongly through your mouth as you spread your arms wide, releasing any tension. Let's try this a few times and feel the release."
            
         ],

         "fear" : [
            
               "I appreciate you taking this step. Let's try Box Breathing—it helps bring steadiness when things feel uncertain. Fear can make breathing shallow and fast, but this method restores control and rhythm. Inhale for 4 seconds… hold for 4… exhale slowly for 4… and hold again for 4. Imagine your breath forming a strong, steady square. Let's do this together and let each breath bring a little more stability.",

               "I appreciate you trying this. Humming Breath can be a simple but powerful way to ease fear. When fear takes over, the vibrations from humming naturally calm the nervous system. Take a deep breath in through your nose. As you exhale, gently hum like a bee, feeling the vibration in your throat. This sound creates a soothing effect that helps relax the body. Let's do this a few times and let the calmness take over.",

               "Great!,  Let's try Candle Breathing—it's a simple way to ease fear and bring focus. Fear can make the mind feel scattered, but controlled breathwork helps bring it back. Imagine a candle in front of you. Inhale deeply through your nose, and then exhale slowly through pursed lips, as if trying to make the flame flicker without putting it out. This slow, steady breath helps calm your mind."
            
         ],
      }
   },
   "Audio_based":[],
   "Visual-Based":{
      "a simple breathing technique":{
         "sad" : [
            
               "I'm really glad you're giving this a try. Belly Breathing can help create a sense of comfort and ease heavy emotions by activating the body's relaxation response. Take a look at the video.  https://youtu.be/OXjlR4mXxSk",

               "Good call. Sighing Breath is great for letting go of tension and emotional weight, helping to reset your nervous system. Check it out here.  https://youtu.be/3xzew29MBwo",

               "You're doing great by taking a step toward feeling better. The 5-5-5 Breathing technique helps bring stability when sadness feels overwhelming by creating a steady rhythm for your breath. Watch the video to try it.  https://youtu.be/Z7Az_iKCBRg"
            
         ],

         "anxious" : [
            
               "It's great that you're open to this. 4-7-8 Breathing naturally slows your heart rate and relaxes the mind by extending your exhales, which signals safety to your body. Take a moment to watch.  https://youtu.be/Uxbdx-SeOOo",

               "It's great that you're taking this moment for yourself. Alternate Nostril Breathing can help settle racing thoughts and restore balance by synchronizing both hemispheres of the brain. Check out the video.  https://youtu.be/G8xIEzX40bA",

               "I'm glad you're giving this a shot. Ocean Breath creates a steady rhythm that soothes the nervous system, helping you feel more in control. Watch how it's done.  https://youtu.be/3xLbkKOyaA0",

               "I really respect that you're giving this a go, Feather Breathing is a simple way to ease tension and regain a sense of control by focusing on slow, gentle exhales. Have a look at the video.  https://youtu.be/p6YAL0ZMkwA"
            
         ],

         "anger" : [
            
               "I appreciate you giving this a try. Cooling Breath can help bring down that inner heat and ease frustration by lowering body temperature and calming the mind. Check it out here.  https://youtu.be/BfKxQ6Jx_i4",

               "It's great that you're open to this. Lion's Breath lets you release built-up energy in a controlled way by engaging the muscles and vocal cords to release tension. Watch the video to try it.  https://youtu.be/CJ9tZL839mI",

               "It's good that you're letting yourself release this tension. Woodchopper Breath is great for releasing tension while staying grounded by pairing breath with movement. Look at how it's done.  https://youtu.be/fc7Q8_nXB2s",

               "It's strong of you to do this. Volcano Breath helps you regain control over strong emotions by using powerful inhales and controlled exhales. Watch the video to try it out.  https://youtu.be/ia0ciWr0aNg"
            
         ],

         "fear" : [
            
               "I appreciate you taking this step. Box Breathing helps steady your breath and ground you when fear makes things feel overwhelming. Take a look at the video.  https://youtu.be/a7uQXDkxEtM",

               "It's great that you're trying this. Humming Breath calms the nervous system by using sound vibrations to bring a sense of peace. Watch the video and give it a try.  https://youtu.be/YTlXxiz42Zg",

               "You're making a great choice by trying this. Candle Breathing helps redirect fearful energy by focusing on slow, gentle exhales, bringing back control. Have a look at the video.  https://youtu.be/ObZ0LzUOL4o"
            
         ],
      }
   },
   "Physical-Activities":[],
   }

   




class ActionSetSuggestion(Action):
   def name(self) -> Text:
      return "action_set_suggestion"

   def run(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        intent = tracker.latest_message['intent']['name']
        emotion = tracker.get_slot("emotion")
        preference = tracker.get_slot("preference")

        if(emotion != "happy"):
            if(intent != "deny"):
               coping_type = random.choice(preference[emotion]) 
               coping_strategy = random.choice(list(cope_dump[coping_type].keys()))
               coping = random.choice(random.choice(coping_strategy[emotion]))
            else:
               coping_strategy = random.choice(coping_type)
               coping = random.choice(coping_strategy)
                
                
        else:
            coping_strategy = random.choice(happy_suggestion)
            help = ""


        return [SlotSet("suggestion", coping_strategy),
                SlotSet("help", coping)
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


