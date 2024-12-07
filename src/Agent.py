import os 
import torch 
import random 
class Agent:
    def __init__(self, turn=0):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        model_file_path = os.path.join(dir_path, 'models/model.pth')
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.main_NN = None 
        # self.load_model(model_file_path)
        self.moves = []
    def load_weight(self, path):
        self.main_NN.load_state_dict(torch.load(path, weights_only=True)) 
    def load_model(self, path):
        self.main_NN = torch.load(path)
    def choose_action(self, observation):
        if len(self.moves) == 0: 
            # sử dụng CNN để đưa ra action phù hợp có dạng (px, rotate_num) 
            action = random.randint(0, 3) 
        return action
        return self.moves.pop(0)