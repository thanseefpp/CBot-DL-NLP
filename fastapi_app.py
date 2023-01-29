###################################### IMPORTING LIBRARIES ############################################
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import json
import torch
import random
from nn_model import NeuralNet
from nlp_nltk import bag_of_words,tokenize

###################################### FASTAPI SETTING UP #############################################

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class model_input(BaseModel):
    ChatInputText : str
    
###################################### IMPORTING AND TRAINING MODEL ####################################

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
model.eval()#evaluating

###################################### API AND RESPONSES ###############################################

@app.get("/")
def home_page():
    return {"Chatbot App Get URL Response"}

bot_name = "Jerry"

@app.post('/user_chat')
def chat_bot_interaction(input_parameters : model_input):
    input_data = input_parameters.json()
    input_dictionary = json.loads(input_data)
    user_input = input_dictionary['ChatInputText']
    if user_input == "quit":
        response = "Nice to Talk to You 😊"
        return {"bot_name" : bot_name,"response" : response}
    user_input = tokenize(user_input)
    x = bag_of_words(user_input,all_words)
    x = x.reshape(1,x.shape[0])
    x = torch.from_numpy(x) #using numpy array
    
    output = model(x)
    _, predicted = torch.max(output,dim=1)
    tag = tags[predicted.item()]
    
    # finding the probability to get more accurate result
    probs = torch.softmax(output,dim=1)
    prob = probs[0][predicted.item()]
    # if the percentage is greater than 75% then it would give a matching answers.
    if prob.item() > 0.75:
        for intent in collected_data['intents']:
            if tag == intent['tag']:
                # taking random response from the collection
                response = random.choice(intent['responses'])
                return {"bot_name" : bot_name,"response" : response}
    else:
        response = "I don't Understand Can you repeat..."
        return {"bot_name" : bot_name,"response" : response}