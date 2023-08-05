from pytorch2keras.converter import pytorch_to_keras
from torch import nn
import torch

class MyTestNet(nn.Module):
    def forward(self, x):
        return x.view(1, 1, -1)

test_net = MyTestNet()
dummy_input = torch.ones([1, 3, 10])
t_model = pytorch_to_keras(test_net, dummy_input, [(3, 10)], verbose=True)
t_model.save('t_model.h5')