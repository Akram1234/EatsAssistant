import numpy as np
import random
from model import vectorize_sentence, model, classes, chatbot_model, load_intents

data = load_intents()

def generate_response(sentence):
    vec = vectorize_sentence(sentence, model)
    results = chatbot_model.predict(np.array([vec]))
    results_index = np.argmax(results)
    tag = classes[results_index]
    if results[0][results_index] > 0.5:
        for intent in data["intents"]:
            if intent["tag"] == tag:
                return random.choice(intent["responses"])
    else:
        return "I am evolving constantly. I apologize that I could not help you with your query. Please give us a call at and our team will be happy to assist"


