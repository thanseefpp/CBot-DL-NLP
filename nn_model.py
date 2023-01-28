import torch.nn as nn


class NeuralNet(nn.Module):
    """
      Here I Have created 3 layers to Train a Neural Network Model.
      - You can Add more layers to get more accurate score.
    """
    def __init__(self,input_size, hidden_size,num_classes):
        # Abstracting a Class, so you should have to call super(className). in order to work our init method
        super(NeuralNet, self).__init__()
        self.layer1 = nn.Linear(input_size,hidden_size)
        self.layer2 = nn.Linear(hidden_size,hidden_size)
        self.layer3 = nn.Linear(hidden_size,num_classes)
        self.relu   = nn.ReLU()
        
    def forward(self,x):
        output = self.layer1(x)
        output = self.relu(output)
        output = self.layer2(output)
        output = self.relu(output)
        output = self.layer3(output)
        # no activation and no soft_max
        return output