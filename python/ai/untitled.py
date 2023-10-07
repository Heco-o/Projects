import torch
from torch import nn

seed = 42
weight = 0.7
bias = 0.3
start = 0
end = 1
step = 0.02
X = torch.arange(start, end, step).unsqueeze(dim=1)
y = weight * X + bias
train_split = int(0.8 * len(X))
X_train, y_train = X[:train_split], y[:train_split]
X_test, y_test = X[train_split:], y[train_split:]

class model(nn.Module):
	def __init__(self):
		super().__init__()
		
		self.weights = nn.Parameter(torch.randn(1, requires_grad=True, dtype=torch.float32))
		self.bias = nn.Parameter(torch.randn(1, requires_grad=True, dtype=torch.float32))
	
	def forward(self, x: torch.Tensor) -> torch.Tensor:
		return self.weights * x + self.bias

torch.manual_seed(seed)
model0 = model()

#with torch.inference_mode():
#	y_preds = model0(X_test)

loss_fn = nn.L1Loss()
optimizer = torch.optim.SGD(params=model0.parameters(), lr=0.01)

epochs = 1000

torch.manual_seed(seed)
for epoch in range(epochs):
	model0.train()
	y_pred = model0(X_train)
	loss = loss_fn(y_pred, y_train)
	optimizer.zero_grad()
	loss.backward()
	optimizer.step()
	
	model0.eval()
	with torch.inference_mode():
		test_pred = model0(X_test)
		test_loss = loss_fn(test_pred, y_test)
	
	if (epoch + 1) % 10 == 0:
		print(f"Epoch: {epoch + 1} | Loss: {loss} | Test loss: {test_loss}")
		print(model0.state_dict(), "\n", sep="")