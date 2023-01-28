import torch
import json
import random
from nn_model import NeuralNet
from nlp_nltk import bag_of_words,tokenize

# importing the Json Model for Training and Testing
with open('ManualDataGenerator/train_data/collection.json', 'r') as f:
    collected_data = json.load(f)
    
#import trainedModel

file_path = 'model/trained_model.pth'
data = torch.load(file_path)

input_size  = data['input_size']
output_size = data['output_size']
hidden_size = data['hidden_size']
all_words   = data['all_words']
tags        = data['tags']
model_state = data['model_state']

device  = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model   = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()


bot_name = "Jerry"
print("Let's Start 😊| type 'quit' to exit")

while True:
    user_input = input("You : ")
    if sentence == "quit":
        break
    sentence = tokenize(user_input)
    x = bag_of_words(sentence,all_words)
    x = x.reshape(1,x.shape[0])
    x = torch.from_numpy() #using numpy array
    
    output = model(x)
    _, predicted = torch.max(output,dim=1)
    tag = tags[predicted.item()]

