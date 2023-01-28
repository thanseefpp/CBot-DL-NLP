######################################## IMPORTING LIBRARIES ###########################################
from nlp_nltk import stem,tokenize,bag_of_words
import json
import numpy as np
import torch
from torch.utils.data import Dataset,DataLoader
from nn_model import NeuralNet
import torch.nn as nn

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
    bag = bag_of_words(tokenized_sentence=pattern,words=all_words)
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
batch_size      = 8
hidden_size     = 8
input_size      = len(X_train[0])
output_size     = len(tags)
learning_rate   = 0.001
number_epochs   = 1000

# Model
dataset         = ChatDataset()
train_loader    = DataLoader(dataset=dataset,batch_size=batch_size,shuffle=True,num_workers=0)

# checking our pc have cuda support(NVIDIA Graphics Feature) else we will use cpu for building Neural Network.
device  = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model   = NeuralNet(input_size,hidden_size,output_size).to(device=device)


# Loss and Optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(),lr=learning_rate)

for epoch in range(number_epochs):
    for (words,labels) in train_loader:
        words   = words.to(device)
        labels  = labels.to(device)
        
        #forward
        outputs = model(words)
        loss    = criterion(outputs,labels)
        
        #backward and optimizer step
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    
    if (epoch + 1) % 100 == 0:
        print(f"Epoch {epoch+1}/{number_epochs}, Loss {loss.item():.4f}")
        
        
print(f"Final Loss {loss.item():.4f}")
