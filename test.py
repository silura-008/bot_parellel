import rasa
from rasa.nlu.model import RasaNLUInterprete

# Load your trained model
model_path = "./models/nlu-20250218-153202-tattered-beta.tar.gz"  # Replace with the actual path to your trained model
interpreter = RasaNLUInterprete(model_path)

# List of test messages for different intents
test_messages = {
    "happy": [
        "I just got engaged! So excited!",
        "I'm finally getting a vacation!",
        "My best friend sent me a surprise gift. I love it!",
        "I got a new puppy today, so happy!",
        "I just finished my project and it turned out perfect!",
        "I met someone new today, and they're so nice!",
        "I'm going on a road trip with my friends this weekend!",
        "I've been feeling great lately, just happy!",
        "I made a huge sale at work today! Feeling so accomplished!",
        "My partner took me on a surprise date. I'm over the moon!"
    ],
    "sad": [
        "My pet passed away, I miss them so much.",
        "I lost my job today. Feeling devastated.",
        "I got rejected from the job I really wanted.",
        "I haven't talked to my friend in weeks. I feel so lonely.",
        "I failed my final exams. I feel worthless.",
        "I was just dumped by my partner. Feeling so sad.",
        "My childhood friend moved far away. I miss them so much.",
        "I haven't been sleeping well. I feel exhausted and sad.",
        "I lost all my work on my laptop today. What a disaster.",
        "I just found out my favorite show got canceled. So disappointed."
    ],
    "anger": [
        "I'm furious with how unfairly I was treated at work.",
        "Someone cut me off in traffic. I'm so angry!",
        "I'm so frustrated with my project, nothing is working!",
        "Why do people always ignore my hard work?",
        "I'm so mad that my plans got canceled last minute!",
        "I can't believe I lost that game because of cheating!",
        "I feel like my efforts are being taken for granted!",
        "I'm so pissed off that I missed the deadline!",
        "I'm angry because nobody is listening to me!",
        "I can't believe someone took credit for my idea!"
    ],
    "anxious": [
        "I have a big presentation tomorrow, and I'm so nervous.",
        "I'm not sure if I'm ready for this new responsibility at work.",
        "What if I mess up during the interview?",
        "I've been feeling really anxious about the future.",
        "I can't stop worrying about everything going wrong.",
        "I'm so nervous about meeting new people tomorrow.",
        "I keep second-guessing everything I do lately.",
        "I'm anxious because I have to talk in front of a large crowd.",
        "I'm scared I'm going to fail my upcoming exam.",
        "I'm feeling a lot of anxiety about an upcoming change in my life."
    ],
    "fear": [
        "I'm scared of what might happen in the future.",
        "I'm terrified that I might fail.",
        "I'm afraid of being judged by others.",
        "I can't stop worrying about what might go wrong.",
        "I have a fear of public speaking.",
        "I'm scared of being alone in the dark.",
        "What if something bad happens to my loved ones?",
        "I'm afraid of taking risks.",
        "I have a deep fear of rejection.",
        "I'm scared I won't be able to achieve my goals."
    ]
}

# Function to test messages
def test_messages_with_model(interpreter, messages):
    for intent, examples in messages.items():
        print(f"\nTesting for intent: {intent}")
        for message in examples:
            result = interpreter.parse(message)
            predicted_intent = result["intent"]["name"]
            confidence = result["intent"]["confidence"]
            print(f"Message: {message}\nPredicted intent: {predicted_intent} (Confidence: {confidence:.2f})\n")

# Run the test
test_messages_with_model(interpreter, test_messages)
