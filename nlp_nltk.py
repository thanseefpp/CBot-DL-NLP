import nltk
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
    pass