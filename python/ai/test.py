import torch
from torch import nn

# Define the function where a and b will be the values you want to predict
def formula(x, a, b):
    return (a / x) * b

# Setting manual a and b for generating synthetic data
true_a = 5.0
true_b = 2.0

# Generate synthetic data
start = 0.1  # Avoiding division by zero
end = 10
step = 0.2
X = torch.arange(start, end, step).unsqueeze(dim=1)  # shape: [n_samples, 1]
y = formula(X, true_a, true_b)

# Split data into training and test sets
train_split = int(0.8 * len(X))
X_train, y_train_true = X[:train_split], y[:train_split]
X_test, y_test_true = X[train_split:], y[train_split:]

# Target for each X is the pair [a, b] to predict both values
y_train = torch.tensor([true_a, true_b]).repeat(len(X_train), 1)  # shape: [len(X_train), 2]
y_test = torch.tensor([true_a, true_b]).repeat(len(X_test), 1)    # shape: [len(X_test), 2]

# Define the model that predicts a and b
class FormulaPredictor(nn.Module):
    def __init__(self):
        super().__init__()
        # Two outputs, one for a and one for b
        self.linear_layer = nn.Linear(in_features=1, out_features=2)
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.linear_layer(x)

# Set manual seed for reproducibility
torch.manual_seed(42)
model = FormulaPredictor()

# Define optimizer and loss function (MSELoss or L1Loss)
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)
loss_fn = nn.MSELoss()  # You can also try nn.L1Loss() for absolute error

epochs = 1000
torch.manual_seed(42)

# Training loop
for epoch in range(epochs):
    model.train()
    
    # Forward pass: predict [a, b] values
    predictions = model(X_train)
    
    # Calculate loss between predicted [a_pred, b_pred] and true [a, b]
    loss = loss_fn(predictions, y_train)
    
    # Backpropagation
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    # Evaluate on test data
    model.eval()
    with torch.no_grad():
        test_predictions = model(X_test)
        test_loss = loss_fn(test_predictions, y_test)
    
    # Print progress every 100 epochs
    if (epoch + 1) % 100 == 0:
        print(f"Epoch: {epoch + 1} | Train Loss: {loss.item()} | Test Loss: {test_loss.item()}")
        print(f"Predicted a, b values (weights): {model.state_dict()}\n")