import os 
import random 
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data import DataLoader, Dataset

# class TetrisCNN(nn.Module):
#     def __init__(self):
#         super(TetrisCNN, self).__init__()
        
    
#         self.conv1 = nn.Conv2d(1, 32, kernel_size=5, stride=5) 
        
     
#         self.conv2 = nn.Conv2d(32, 64, kernel_size=3, stride=2, padding=1) 
        
       
#         self.conv3 = nn.Conv2d(64, 128, kernel_size=3, stride=2, padding=1) 
        
#         # Flatten layer
#         self.flatten = nn.Flatten()
        
#         # Fully connected layers
#         self.fc1 = nn.Linear(128, 512)  # Adjusted input size
#         self.fc2 = nn.Linear(512, 256)
#         self.fc3 = nn.Linear(256, 44)
        
#     def forward(self, x):
#         # Convolutional layers with ReLU activation
#         x = F.tanh(self.conv1(x))  # Using ReLU instead of tanh
#         # print(x.size())
#         x = F.tanh(self.conv2(x))  # Using ReLU instead of tanh
#         # print(x.size())
#         x = F.tanh(self.conv3(x))  # Using ReLU instead of tanh
#         # print(x.size())
#         # Flatten the output
#         x = self.flatten(x)
        
#         # Fully connected layers with ReLU
#         x = F.tanh(self.fc1(x))  # Using ReLU instead of tanh
#         x = F.tanh(self.fc2(x))  # Using ReLU instead of tanh
#         x = self.fc3(x)  # Output layer, no ReLU
        
#         return x
class TetrisCNN(nn.Module):
    def __init__(self):
        super(TetrisCNN, self).__init__()
        
    
        self.conv1 = nn.Conv2d(1, 32, kernel_size=5, stride=5) 
        
     
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, stride=2, padding=1) 
        
       
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, stride=2, padding=1) 
        
        # Flatten layer
        self.flatten = nn.Flatten()
        
        # Fully connected layers
        self.fc1 = nn.Linear(128, 512)  # Adjusted input size
        self.fc2 = nn.Linear(512, 256)
        self.fc3 = nn.Linear(256, 44)
        
    def forward(self, x):
        # Convolutional layers with ReLU activation
        x = F.relu(self.conv1(x))  # Using ReLU instead of relu
        # print(x.size())
        x = F.relu(self.conv2(x))  # Using ReLU instead of relu
        # print(x.size())
        x = F.relu(self.conv3(x))  # Using ReLU instead of relu
        # print(x.size())
        # Flatten the output
        x = self.flatten(x)
        
        # Fully connected layers with ReLU
        x = F.relu(self.fc1(x))  # Using ReLU instead of relu
        x = F.relu(self.fc2(x))  # Using ReLU instead of relu
        x = self.fc3(x)  # Output layer, no ReLU
        
        return x
class Agent:
    def __init__(self, turn=0):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        model_file_path = "/home/quangai/game_ai_pytorch/TETRIS_CNN/CNN_GAME/src/models/weights_1000_epochs.pth"
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.main_NN = TetrisCNN().to(self.device)
        self.load_weight(model_file_path)
        self.moves = []
        self.dict_action = {}
        cnt = 0
        for i in range(0, 11):
            for j in range(0, 4):
                self.dict_action[cnt] = i * 10 + j 
                cnt += 1
    def load_weight(self, path):
        self.main_NN.load_state_dict(torch.load(path, weights_only=True)) 
    def load_model(self, path):
        self.main_NN = torch.load(path)
    def choose_action(self, states):
        if len(self.moves) == 0:
            # sử dụng CNN để đưa ra action phù hợp có dạng (px, rotate_num)
            check_states = states
            states = torch.FloatTensor(states).to(self.device)  # 1 x input_size
            states = states.unsqueeze(0)
            states = states.unsqueeze(1)  # Thêm chiều kênh vào
            # print(states.shape)
            self.main_NN.eval()
            with torch.no_grad():
                outputs = self.main_NN(states)
                _, predicted = torch.max(F.softmax(outputs, dim=1), 1)
                # print("val: ", predicted.item()) 
                predicted = self.dict_action[predicted.item()]
                px_best, rotate_best = predicted // 10 - 2, predicted % 10

            """
                rotate_best == 0 => rotate right 0 turn
                rotate_best == 1 => rotate right 1 turn
                rotate_best == 2 => rotate right 2 turn
                rotate_best == 3 => rotate right 3 turn
            """
            num_rotate = rotate_best
            px = 3  # Vị trí mặc định của 1 khối
            # print(px_best, rotate_best)
            # print(check_states)
            for n_r in range(num_rotate):  # Quay theo số lần
                self.moves.append(1)  # Lệnh quay phải

            if px_best > px:  # Di chuyển sang phải
                for _ in range(px_best - px):
                    self.moves.append(2)  # Lệnh di chuyển phải
            elif px_best < px:  # Di chuyển sang trái
                for _ in range(px - px_best):
                    self.moves.append(3)  # Lệnh di chuyển trái

            # Cuối cùng, thả khối
            self.moves.append(0)  # Lệnh thả    

        return self.moves.pop(0)  # Trả về hành động tiếp theo