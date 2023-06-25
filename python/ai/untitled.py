import torch

rand_tensor0 = torch.rand((3,2))
rand_tensor1 = torch.rand((3,5))
rand_tensor2 = torch.rand((3,3))
print(rand_tensor0)
print(rand_tensor1)
print(rand_tensor2)
print()
t0 = torch.cat([rand_tensor2, rand_tensor2, rand_tensor2], dim=1)
print(t0)