import torch
from torch import nn
from torch.nn import functional


class GlobalPooling(nn.Module):
    def forward(self, x: torch.Tensor):
        return functional.adaptive_avg_pool2d(x, 1).view(x.size(0), -1)


class InplaceReLU6(nn.ReLU6):
    def __init__(self):
        super().__init__(inplace=True)
