import json
import numpy as np
import nltk
import gensim.downloader as api
from tensorflow.keras.models import load_model
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

model = api.load("word2vec-google-news-300")
chatbot_model = load_model('../Data/EatsAdvisor_word2vec.h5')
lemmatizer = WordNetLemmatizer()

def vectorize_sentence(sentence, model):
    sentence = sentence.rstrip("?")
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower(), pos='v') for word in sentence_words if word not in set(stopwords.words("english"))]
    vecs = []
    for word in sentence_words:
        if word in model.key_to_index:
            vecs.append(model[word])
    if vecs:
        vecs = np.mean(vecs, axis=0)
    else:
        vecs = np.zeros(model.vector_size)
    return vecs

def load_intents():
    with open("../Data/intents.json", "r") as f:
        return json.load(f)

classes = [intent["tag"] for intent in load_intents()["intents"]]
