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
        personality ="new"
        preference = {
            "sad": ["Visual-Based", "Audio-Based", "Text-Based", "Physical-Activities"],
            "anger": ["Visual-Based", "Audio-Based", "Text-Based", "Physical-Activities"],
            "anxious": ["Visual-Based", "Audio-Based", "Text-Based", "Physical-Activities"],
            "fear": ["Visual-Based", "Audio-Based", "Text-Based", "Physical-Activities"]
        }
         
        help_line =988
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
            preference = {
               "sad": ["Visual-Based", "Audio-Based", "Text-Based", "Physical-Activities"],
               "anger": ["Visual-Based", "Audio-Based", "Text-Based", "Physical-Activities"],
               "anxious": ["Visual-Based", "Audio-Based", "Text-Based", "Physical-Activities"],
               "fear": ["Visual-Based", "Audio-Based", "Text-Based", "Physical-Activities"]
            }
            
            help_line =988

        # Set slots before the conversation starts
        return [
            SessionStarted(),
            SlotSet("personality", personality),
            SlotSet("preference", preference),
            SlotSet("help_line", help_line),
            ActionExecuted("action_listen"), 
        ]

cope_dump = {
   "Text-Based":{
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
      },
      "an insightful article": {
         "anger": [
                  "You're doing great by addressing your emotions. Managing anger isn't about suppressing it but expressing it in a healthy way. This guide covers practical techniques: https://www.healthline.com/health/mental-health/how-to-control-anger",
                  "Taking steps to understand anger is powerful! This resource from the American Psychological Association explains strategies for control: https://www.apa.org/topics/anger/strategies-controlling",
                  "You're on the right track! This article provides a science-backed approach to anger management: https://positivepsychology.com/anger-management-techniques/",
                  "Recognizing anger is the first step! Learn about what triggers it and how to deal with it: https://www.medicalnewstoday.com/articles/162035",
                  "Great! WebMD outlines professional anger management strategies: https://www.webmd.com/mental-health/anger-management",
                  "You're taking the right step! Learn mindfulness-based approaches to calming anger here: https://www.calm.com/blog/steps-to-calming-anger"
            ],

         "anxious": [
                  "You're making the right choice! Breathing exercises are scientifically proven to reduce anxiety. Check these out: https://blog.calm.com/breathing-exercises-for-anxiety",
                  "Great! This article outlines immediate ways to manage anxiety and regain control: https://www.healthline.com/health/how-to-calm-anxiety",
                  "You're taking the right step! Discover 16 natural ways to relieve stress and anxiety: https://www.healthline.com/nutrition/16-ways-relieve-stress-anxiety",
                  "You're handling this well! Learn expert-approved ways to naturally lower anxiety levels: https://www.medicalnewstoday.com/articles/326115",
                  "It's great that you're working on this! Explore natural techniques for long-term anxiety relief: https://www.healthline.com/health/natural-ways-to-reduce-anxiety"
            ],

         "sad": [
                  "You're taking the right step! Learn expert-backed ways to navigate sadness: https://www.talkspace.com/blog/how-to-deal-with-sadness/",
                  "Great! This is a great choice! Here are structured strategies to release sadness effectively: https://www.linkedin.com/pulse/strategies-can-help-you-release-sadness-kal-patel",
                  "You're moving in the right direction! Gundersen Health provides a structured guide to managing sadness: https://www.gundersenhealth.org/health-wellness/mental-health-relationships/healthy-ways-to-deal-with-sadness",
                  "You're taking the right step! Mindfulness-based techniques can shift emotions gently. Learn more here: https://www.calm.com/blog/how-to-stop-feeling-sad",
                  "Taking small steps can lead to big changes. Here's a professional breakdown of coping with sadness: https://healtreatmentcenters.com/mental-health/how-to-deal-with-sadness/"
            ],

         "fear": [
                  "You're facing your fears head-on, and that's commendable! NHS provides a step-by-step guide to managing fear: https://www.nhsinform.scot/healthy-living/mental-wellbeing/fears-and-phobias/10-ways-to-fight-your-fears/",
                  "Acknowledging fear is the first step! This article breaks down the psychology of fear: https://dazedbysunny.medium.com/an-article-about-fear-79a68ec88c88",
                  "You're being brave! Science explains how fear impacts the brain and how to rewire responses: https://www.sciencedirect.com/science/article/abs/pii/S0306452211013443",
                  "You're tackling this well! Therapy-based techniques can help overcome fear step by step: https://www.choosingtherapy.com/how-to-overcome-fear/"
            ],
      },  
   },
   "Audio_based":{
      "a calming audio guide": {
         "anger": [
            "I'm glad you're taking this step to understand and manage anger in a healthy way. Listening to guided insights can provide new perspectives and techniques to regain control when emotions run high. This audio explores different ways to process and release anger constructively, helping you respond rather than react. Listen here : https://open.spotify.com/show/56iaHI3hHIAcqW6D6upalE"
         ],
         "anxious": [
            "It's great that you're open to exploring ways to ease anxiety. Having a guide can make a difference in navigating those overwhelming moments. This audio provides practical techniques to manage anxiety, covering everything from breathwork to mindset shifts. It helps build resilience and calmness in day-to-day life. Listen here : https://open.spotify.com/show/5UsxoX6ikTr3ETvzQAHbdP",
            
            "I appreciate you taking the time to focus on yourself. Understanding anxiety is a powerful first step toward managing it effectively. This audio is designed for high achievers who struggle with high-functioning anxiety, offering ways to feel more balanced, confident, and at ease. Listen here : https://open.spotify.com/show/0gahU19SN8cT3fkotPwzT5",
            
            "It's strong of you to take a moment to work through anxious thoughts. Having a knowledgeable guide can make all the difference. Hosted by a psychotherapist specializing in anxiety, this audio offers expert strategies to ease fear, stress, and overwhelming emotions in daily life. Listen here : https://open.spotify.com/show/7wQlyLJ8DorFkI41mT3EEF"
         ],
         "sad": [
            "I appreciate you for doing this. Taking time to explore and process emotions can be a meaningful step toward healing. This audio provides gentle guidance on navigating emotions like sadness, offering practical exercises and reflections to bring clarity and peace. Listen here : https://open.spotify.com/show/3Z9pPvKcxEksVstTt1x3nY",
            
            "It's strong of you to take a moment to work through this. Humor can sometimes bring light to even the heaviest feelings. This audio blends comedy with candid discussions about depression, helping to normalize emotions and offer a refreshing perspective on mental well-being. Listen here : https://open.spotify.com/show/3Z9pPvKcxEksVstTt1x3nY"
         ],
         "fear": [
            "I appreciate you taking this step. Facing fear and past emotional wounds can be challenging, but it's also a sign of strength. This audio provides tools for healing fear, emotional wounds, and trauma, offering practical guidance to move forward with resilience. Listen here : https://open.spotify.com/show/4n7mVBjNRjWgiXALoy2zXS"
         ],
      },
   },
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
      },
      "a guided video session" : {
         "anxious": [
                  "You're taking the right step! These techniques can help manage anxiety and restore calm. Check them out: https://youtu.be/WWloIAQpMcQ",
                  "It's great that you're open to this! Here are some practical ways to ground yourself and reduce anxious feelings: https://youtu.be/Q2sixA1vPKk",
                  "Nice move! This video guides you through body-based methods to ease anxiety: https://youtu.be/HseTZkLLS_c",
                  "gREAT! Try these techniques to slow down racing thoughts: https://youtu.be/ScpDOm08wx8"
            ],
         "fear": [
                  "Good! Facing fear starts with small steps. Check out these techniques to regain control: https://youtu.be/Q2sixA1vPKk",
                  "It's great that you're open to this! These strategies help shift fear into confidence: https://youtu.be/nX4dpGQ5wF4",
                  "You're taking the right step! Watch this video for ways to calm the nervous system when fear takes over: https://youtu.be/CPdBWXiRTaI"
            ],
         "anger": [
                  "You're choosing a healthy way to release anger! Here are some powerful techniques to manage frustration: https://youtu.be/H4WYp9a6Yzg",
                  "Great call! These strategies help you process anger constructively: https://youtu.be/Yh1-y3TzSO4",
                  "You're taking the right step! Watch how small actions can help you cool down: https://youtu.be/BsVq5R_F6RA",
                  "It's great that you're open to this! This video guides you through calming techniques for anger: https://youtu.be/kZWhem4kiwE",
                  "Great! These exercises help release tension and regain clarity: https://youtu.be/F22ZvJR2mss"
            ],
         "sad": [
                  "You're taking the right step! This video shares ways to lift your mood: https://youtu.be/HvSOHmqWMAw",
                  "You're doing the right thing by addressing your emotions. Check out these helpful strategies: https://youtu.be/ph8av8MQ29I",
                  "Nice! These tips can help you reconnect with yourself and find comfort: https://youtu.be/3bEA4ejqVfk",
                  "It's great that you're open to this! Watch this for some useful guidance: https://youtu.be/ZBOZKSvkr-o"
            ],
      },
   },
   "Physical-Activities":{
         "a quick energizing activity" : {
            "sad": [
                     "Great job for giving this a try! When sadness weighs you down, gentle movement and self-soothing actions can help lift some of that heaviness. Let's do Rhythmic Self-Tapping—gently tap your arms, legs, and shoulders in a steady rhythm. It reconnects you with your body and brings a sense of comfort.",
                     "Nice! Holding certain positions can give your nervous system a break from emotional overload. Try Forward Bend Hold—stand or sit, slowly bend forward, and let your arms hang loose. It naturally soothes and releases emotional tension.",
                     "You're doing great! Deep-pressure stimulation can be really comforting when you're feeling down. Let's try Hug Compression Hold—cross your arms over your chest and squeeze firmly. This mimics a reassuring hug and provides a calming effect.",
                     "You're taking the right step! Sometimes, grounding with physical weight can bring emotional stability. Try Weighted Object Hold—hold a moderately heavy object (like a book or kettlebell) close to your chest for a minute. The added pressure creates a sense of security.",
                     "You got this! Slow, rhythmic movement can gently lift your energy levels. Let's do Cross-Lateral Marching—raise your right knee and touch it with your left hand, then switch. This stimulates coordination and slowly energizes you.",
                     "Great! Slight muscle engagement can counteract emotional numbness. Try Wall Sit Hold—press your back against a wall, lower into a sitting position, and hold for 20-30 seconds. This helps you feel grounded and present."
               ],
            "anxious": [
                     "Well done for taking control! Anxiety often gets stored as physical tension, so let's release some of it. Try Butterfly Hug Tapping—cross your arms and alternately tap your shoulders. This self-soothing technique regulates the nervous system and provides instant relief.",
                     "Nice! Releasing built-up tension in the muscles can also release anxious energy. Let's do Progressive Muscle Tensing—clench your fists for 5 seconds, then release. Repeat with your shoulders, legs, and feet. It helps discharge tension and brings calmness.",
                     "You're taking a solid step in easing anxiety! Small, repetitive motions can interrupt racing thoughts. Try Finger Tapping Sequences—tap each fingertip to your thumb in a set pattern. This keeps your mind engaged and reduces overthinking.",
                     "Great! Anxiety often makes you feel disconnected, but grounding exercises help. Let's do Heel Raises—slowly lift your heels off the ground, then lower them back down. This keeps you present and stabilizes your energy.",
                     "You're taking the right step! Slight pressure can have a grounding effect. Try Cross-Body Shoulder Press—press one hand firmly against the opposite shoulder and hold. It brings an immediate sense of calm.",
                     "Nice! Gentle shifting movements can help bring balance back to your nervous system. Let's do Standing Weight Shifting—stand with feet hip-width apart and gently shift your weight from one foot to the other. This reestablishes stability and focus."
               ],
            "anger": [
                     "Way to channel that energy in a healthy way! Anger needs an outlet, and controlled exertion can help. Try Pillow Punching—grab a pillow and punch it as hard as you can for a set time. It allows frustration to be expressed safely.",
                     "Smart move! Pressing against a solid surface gives your body a safe way to exert energy. Let's do Isometric Wall Pushes—press both hands against a wall and push with all your strength for 5-10 seconds, then release. This mimics an outlet for frustration.",
                     "You're handling this well! Twisting motions help release stored aggression in the body. Try Woodchopper Twists—stand with feet apart, clasp hands together, and swing them diagonally down as if chopping wood. It's a great way to move anger through your system.",
                     "You're taking the right step! Repetitive force-based movements are excellent for releasing aggression. Let's try Sledgehammer Slams (if accessible)—use a sledgehammer or heavy object to strike a tire or padded surface. This helps channel frustration constructively.",
                     "I see you're ready to release some tension! Twisting motions can help express pent-up anger. Try Resisted Towel Twisting—hold a towel in both hands and twist it tightly as if wringing out water. This engages tension and provides an outlet.",
                     "Great decision! High-energy exercises are ideal for letting go of anger. Let's do Jump Squats—explode upward from a squat position and land back into a squat. This intense movement helps release frustration while keeping control."
               ],
            "fear": [
                     "You're taking the right step! Fear makes the body feel unsteady, so grounding is key. Try Grounding Stomps—firmly stomp your feet against the floor a few times. This sends signals of stability to your nervous system and reinforces control.",
                     "Great! Balance exercises build a sense of inner steadiness. Let's do Single-Leg Balancing—lift one foot slightly off the ground and hold. This strengthens focus and counteracts feelings of uncertainty.",
                     "Nice! Controlled resistance builds a sense of security. Try Isometric Presses—press your palms firmly together or push against a solid surface. This engages muscles and helps reinforce inner strength.",
                     "This is a great step! Coordinated movements break the cycle of fear. Let's try Cross-Body Reaches—extend your right arm toward your left foot, then switch. This helps engage coordination and disrupt fear-driven thought patterns.",
                     "You're taking charge! Controlled descent exercises train your mind to feel safer. Try Slow Step Downs—stand on a step or platform, lower one foot down slowly, then return. This reinforces a sense of safety and control.",
                     "Proud of you! Posture can influence emotional strength. Let's do Power Stance Hold—stand with feet wide apart, hands on hips, and chest lifted. Holding this strong posture sends confidence signals to your brain and reduces vulnerability."
               ],
         },
   },
}

suggestions = {
    "an insightful article" :["an insightful article","a thoughtful read", "a self help resource","a calming read","a guiding article"],
    "a guided video session" :["a guided video session","a helpful visual guide","a calming watch","a gentle video walkthrough"],
    "a simple breathing technique":["a simple breathing technique","A gentle breathwork session","a deep relaxation breath","a centering breath practice"],
    "a calming audio guide":["a calming audio guide","an audio check-in",],
    "a quick energizing activity":["a quick energizing activity","a simple physical ascivity","a slow and steady movment","a centering movement"],
}
   
happy_suggestion = ["talking to a friend about it","write it down in your journal","share in your social media"]

happy_responses = {
    "talking to a friend about it": [
        "Great! Sharing with a friend makes the moment even more meaningful.",
        "Wonderful! A conversation can make your happiness even more real.",
        "Awesome! Connecting with someone makes happy moments even better.",
        "Fantastic! Sharing happiness strengthens bonds."
    ],
    "writing it down in your journal": [
        "Brilliant! Writing it down helps keep the memory alive.",
        "Wonderful! Journaling makes the feeling last longer.",
        "Amazing! Capturing the moment in words makes it timeless.",
        "Fantastic! Your journal will hold this joy forever.",
        "Great! Recording happiness makes it even more special."
    ],
    "sharing it on social media": [
        "Awesome! Spreading positivity is always wonderful.",
        "Fantastic! Celebrating moments makes them even more special.",
        "Brilliant! Your happiness might brighten someone else's day.",
        "Wonderful! Sharing joy makes the world a happier place.",
        "Amazing! A little positivity on social media is always welcome."
    ]
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
               suggestion = random.choice(suggestions[coping_strategy])
               help = random.choice(cope_dump[coping_type][coping_strategy][emotion])
            else:
               suggestion= "a simple breathing technique"
               help = random.choice(cope_dump["Text-Based"]["a simple breathing technique"][emotion])
               
                
        else:
            suggestion = random.choice(happy_suggestion)
            help = random.choice(happy_responses[suggestion])


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


