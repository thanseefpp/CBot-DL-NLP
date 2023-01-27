import nltk
import numpy as np
from nltk.stem.porter import PorterStemmer
# nltk.download('punkt') uncomment this for first time only. if you don't have the package.


stemmer = PorterStemmer()

# Tokenizing
def tokenize(sentence):
    return nltk.word_tokenize(sentence)
  
# Stemming words
def stem(word):
    return stemmer.stem(word=word.lower())

def bag_of_words(tokenized_sentence,all_words):
    """
    sentence = ['Hai','Hello',"How","are","you"]
    words = ["Hi","Hai","Hello","Jump","Jet","Are","wait","You"]
    output = [0,1,1,0,0,1,0,1]
    """
    tokenized_sentence = [stem(word) for word in tokenized_sentence]
    bag = np.zeros(len(all_words),dtype=float)
    for idx,w in enumerate(all_words):
        if w.lower() in tokenized_sentence:
            bag[idx] = 1.0
    return bag


# sentence = ["Hai","Hello","How","are","you"]
# words = ["Hi","Hai","Hello","Jump","Jet","Are","wait","You"]
# output = [0,1,1,0,0,1,0,1]
# bag = bag_of_words(sentence,words)
# print(bag)