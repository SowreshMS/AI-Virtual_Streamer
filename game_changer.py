import torch
import torch.nn as nn

class BiLSTM(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, num_classes):
        super(BiLSTM, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.embedding = nn.Embedding(200, 128)

        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True, bidirectional=True)

        self.fc = nn.Linear(hidden_size*2, num_classes)

    def forward(self, x):
        # Initialize hidden state with zeros
        h0 = torch.zeros(self.num_layers*2, x.size(0), self.hidden_size).to(device)
        c0 = torch.zeros(self.num_layers*2, x.size(0), self.hidden_size).to(device)

        x = self.embedding(x)

        out, _ = self.lstm(x, (h0, c0))

        out = self.fc(out[:, -1, :])

        return out

device = 'cuda' if torch.cuda.is_available() else 'cpu'

input_size = 128
hidden_size = 128
num_layers = 2
num_classes = 5

model = BiLSTM(input_size, hidden_size, num_layers, num_classes)

class Model():
    def __init__(self):
        # initializing our pytorch model
        self.model = torch.load(r"C:\Users\Spher\OneDrive\Desktop\CS\AI\Kuebiko\model.pth")
    
    def __call__(self, input):
        # converting each character in input to an integer and storing it in ty
        ty = []
        for i in input:
            ty.append(ord(i))
        
        output = self.model(torch.tensor(ty).unsqueeze(0).cuda())

        probs = nn.Softmax(dim=1)(output)

        print(probs)
        
        return torch.argmax(probs, dim=1).item() if torch.max(probs, dim=1)[0].item() > 0.5 else 4

