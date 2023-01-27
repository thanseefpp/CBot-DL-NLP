######################################## IMPORTING LIBRARIES ###########################################
from nlp_nltk import stem,tokenize,bag_of_words
import json
import datetime
import numpy as np
import torch
from torch.utils.data import Dataset,DataLoader
start_time = datetime.datetime.now()

######################################### MODEL IMPORT #################################################
# importing the Json Model for Training and Testing
with open('ManualDataGenerator/train_data/collection.json', 'r') as f:
    collected_data = json.load(f)

######################################### FUNCTIONS HANDLING #################################################
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
all_words = [stem(word) for word in all_words if word not in invalid_words]
all_words = sorted(set(all_words))  
tags = sorted(set(tags))

######################################### TRAINING MODEL #################################################

X_train = []
y_train = []

for (patterns,tag) in Xy:
    bag = bag_of_words(tokenized_sentence=pattern,all_words=all_words)
    X_train.append(bag)
    labeled = tags.index(tag)
    y_train.append(labeled) # to get the tag here manual encoding using the index values to get the actual tag value.
    

# convert to two dimensional Array

X_train = np.asarray(X_train)
y_train = np.asarray(y_train)


class ChatDataset(Dataset):
    def __init__(self):
        self.n_samples = len(X_train)
        self.x_data = X_train
        self.y_data = y_train
        
    def __len__(self):
        return self.n_samples
    
    def __getitem__(self, index):
        return self.x_data[index],self.y_data[index]
    

# Hyperparameter
batch_size = 8

dataset = ChatDataset()
train_loader = DataLoader(dataset=dataset,batch_size=batch_size,shuffle=True,num_workers=2)


print(f'start time : {start_time}')
end_time = datetime.datetime.now()
print(f"end_time : {end_time}")
print(f"Total Time Taken :{end_time - start_time}")