import torch
from torch import nn

seed = 42
s = 0
n = 21
data = [[i, j] for i in range(s, n) for j in range(s, n)]
label = [i[0] - i[1] for i in data]

X = torch.tensor(data, dtype=torch.float32)
y = torch.tensor(label, dtype=torch.float32).view(-1, 1)

train_split = int(0.8 * len(X))
X_train, X_test = X[:train_split], X[train_split:]
y_train, y_test = y[:train_split], y[train_split:]

def accuracy_fn(y_true, y_pred):
	correct = torch.eq(y_true, y_pred).sum().item()
	acc = (correct / len(y_pred)) * 100 
	return acc

class modelV2(nn.Module):
	def __init__(self):
		super().__init__()
		self.layer_1 = nn.Linear(in_features=2, out_features=10)
		self.layer_2 = nn.Linear(in_features=10, out_features=10)
		self.layer_3 = nn.Linear(in_features=10, out_features=1)
	
	def forward(self, x: torch.Tensor) -> torch.Tensor:
		#return self.layer_5(self.layer_4(self.layer_3(self.layer_2(self.layer_1(x)))))
		return self.layer_3(self.layer_2(self.layer_1(x)))

torch.manual_seed(seed)
model0 = modelV2()

model0.load_state_dict(torch.load('model.pth'))

loss_fn = nn.L1Loss()
optimizer = torch.optim.SGD(params=model0.parameters(), lr=0.00000000001)

#loss_fn = nn.BCEWithLogitsLoss()
#optimizer = torch.optim.Adam(params=model0.parameters(), lr=0.00001)

epochs = 100000
torch.manual_seed(seed)
for epoch in range(epochs):
	model0.train()
	y_pred = model0(X_train)
	loss = loss_fn(y_pred, y_train)
	acc = accuracy_fn(y_true=y_train, y_pred=y_pred) 
	optimizer.zero_grad()
	loss.backward()
	optimizer.step()
	
	model0.eval()
	with torch.inference_mode():
		test_pred = model0(X_test)
		test_loss = loss_fn(test_pred, y_test)
		test_acc = accuracy_fn(y_true=y_test, y_pred=test_pred)
	
	if (epoch + 1) % 100 == 0:
		print(f"Epoch: {epoch + 1} | Loss: {loss:.5f}, Accuracy: {acc:.2f}% | Test loss: {test_loss:.5f}, Test acc: {test_acc:.2f}%")
		#print(model0.state_dict(), "\n", sep="")
	torch.save(model0.state_dict(), 'model.pth')

with torch.inference_mode():
	test000_pred = model0(X_test)
	for i in range(len(X_test)):
		print(f"{X_test[i]}: {test000_pred[i]}, {y_test[i]}")

torch.save(model0.state_dict(), 'model.pth')