from nlp_nltk import stem,tokenize,bag_of_words
import json


# importing the Json Model for Training and Testing

with open('ManualDataGenerator/train_data/collection.json', 'r') as f:
    collected_data = json.load(f)
    


all_words =  []
tags = []
Xy = []


for item in collected_data['intents']:
    tag = item['tag']
    tags.append(tag) 
    for pattern in item['patterns']:
        word = tokenize(pattern)
        all_words.extend(word)
        Xy.append((word,tag))
        
invalid_words = ['@','!',',','"',':',";",' ','.','#',"_","-",'+'] # you can add more symbols to avoid from the words

# print(f"Before : {all_words} len:{len(all_words)}")

all_words = [stem(word) for word in all_words if word not in invalid_words]

# print(f"After : {all_words} len:{len(all_words)}")
    