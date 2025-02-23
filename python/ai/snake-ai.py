from collections import deque
import threading
import curses
import random
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import time
import os

val0 = []
columns, lines = os.get_terminal_size()
lines -= 1
possiblePos = {(i, j) for i in range(columns) for j in range(lines)}

Round = 0
ticks = 0
bestScore = 0

gameNotOver = True

#headsPos = set()
partsPos = set()
foodsPos = set()

foods = {}
snakes = []

stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)
stdscr.nodelay(True)

lock1 = threading.Lock()

class Head:
	base = "^"
	bases = ["^", "v", "<", ">"]
	
	def __init__(self, directionX = 0, directionY = -1, posX = 0, posY = 0):
		self._directionX = directionX
		self._directionY = directionY
		self._posX = self.pastPosX = posX
		self._posY = self.pastPosY = posY
		#headsPos.add((self._posX, self._posY))
		partsPos.add((self._posX, self._posY))
		self.update_base()
	
	@property
	def directionX(self):
		return self._directionX

	@property
	def directionY(self):
		return self._directionY

	@directionX.setter
	def directionX(self, value):
		self._directionX = value
		self._directionY = 0
		self.update_base()

	@directionY.setter
	def directionY(self, value):
		self._directionX = 0
		self._directionY = value
		self.update_base()
	
	@property
	def posX(self):
		return self._posX
	
	@property
	def posY(self):
		return self._posY
	
	@posX.setter
	def posX(self, value):
		#headsPos.remove((self._posX, self._posY))
		partsPos.remove((self._posX, self._posY))
		self.pastPosX = self._posX
		self.pastPosY = self._posY
		self._posX = value
		#headsPos.add((self._posX, self._posY))
		partsPos.add((self._posX, self._posY))
	
	@posY.setter
	def posY(self, value):
		#headsPos.remove((self._posX, self._posY))
		partsPos.remove((self._posX, self._posY))
		self.pastPosX = self._posX
		self.pastPosY = self._posY
		self._posY = value
		#headsPos.add((self._posX, self._posY))
		partsPos.add((self._posX, self._posY))
	
	def update_base(self):
		if self._directionX == 1:
			self.base = self.bases[3]
		elif self._directionX == -1:
			self.base = self.bases[2]
		elif self._directionY == 1:
			self.base = self.bases[1]
		elif self._directionY == -1:
			self.base = self.bases[0]

class Part:
	base = "#"
	
	def __init__(self, posX = 0, posY = 0):
		if posX == -1: self.posX = self.pastPosX = columns - 1
		elif posX == columns: self.posX = self.pastPosX = 0
		else: self.posX = self.pastPosX = posX
		
		if posY == -1: self.posY = self.pastPosY = lines - 1
		elif posY == lines: self.posY = self.pastPosY = 0
		else: self.posY = self.pastPosY = posY
		
		partsPos.add((self.posX, self.posY))
	
	def set(self, posX, posY):
		partsPos.remove((self.posX, self.posY))
		self.pastPosX = self.posX
		self.pastPosY = self.posY
		self.posX = posX
		self.posY = posY
		partsPos.add((self.posX, self.posY))

class Food:
	base = "@"
	
	def __init__(self, posX = None, posY = None):
		availPos = possiblePos - partsPos - foodsPos
		if posX == None and posY == None:
			availPos = random.choice(list(availPos))
			self.posX = availPos[0]
			self.posY = availPos[1]
		elif (posX == None) ^ (posY == None):
			if posX != None: availPos = {pos for pos in availPos if pos[0] == posX}
			elif posY != None: availPos = {pos for pos in availPos if pos[1] == posY}
			availPos = random.choice(list(availPos))
			self.posX = availPos[0]
			self.posY = availPos[1]
		else:
			self.posX = posX
			self.posY = posY
		
		foods[(self.posX, self.posY)] = self
		foodsPos.add((self.posX, self.posY))
	
	def ate(self, posX = None, posY = None):
		foods.pop((self.posX, self.posY))
		foodsPos.remove((self.posX, self.posY))
		Food(posX, posY)

class Snake:
	def __init__(self, directionX = 0, directionY = -1, posX = int(columns/2), posY = int(lines/2)):
		self.foodAte = self.gameOver = False
		self.parts = []
		self.score = 0
		
		self.head = Head(directionX, directionY, posX, posY)
		self.parts.append(self.head)
		snakes.append(self)
	
	def nextH(self):
		if self.head.directionY == 0:
			if self.head.posX == 0 and self.head.directionX == -1:
				if (columns - 1, self.head.posY) in partsPos: self.gameOver = True
				if (columns - 1, self.head.posY) in foodsPos: self.foodAte = True
				
				self.head.posX = columns - 1
			elif self.head.posX == columns - 1 and self.head.directionX == 1:
				if (0, self.head.posY) in partsPos: self.gameOver = True
				if (0, self.head.posY) in foodsPos: self.foodAte = True
				
				self.head.posX = 0
			else:
				if (self.head.posX + self.head.directionX, self.head.posY) in partsPos: self.gameOver = True
				if (self.head.posX + self.head.directionX, self.head.posY) in foodsPos: self.foodAte = True
				
				self.head.posX += self.head.directionX
		elif self.head.directionX == 0:
			if self.head.posY == 0 and self.head.directionY == -1:
				if (self.head.posX, lines - 1) in partsPos: self.gameOver = True
				if (self.head.posX, lines - 1) in foodsPos: self.foodAte = True
				
				self.head.posY = lines - 1
			elif self.head.posY == lines - 1 and self.head.directionY == 1:
				if (self.head.posX, 0) in partsPos: self.gameOver = True
				if (self.head.posX, 0) in foodsPos: self.foodAte = True
				
				self.head.posY = 0
			else:
				if (self.head.posX, self.head.posY + self.head.directionY) in partsPos: self.gameOver = True
				if (self.head.posX, self.head.posY + self.head.directionY) in foodsPos: self.foodAte = True
				
				self.head.posY += self.head.directionY
	
	def nextP(self):
		for i in range(1, len(self.parts)):
			self.parts[i].set(self.parts[i - 1].pastPosX, self.parts[i - 1].pastPosY)
	
	def generatePart(self):
		currentSize = len(self.parts) - 1
		self.parts.append(Part(self.parts[currentSize].pastPosX, self.parts[currentSize].pastPosY))
	
	def update(self):
		self.nextH()
		self.nextP()
		if self.foodAte:
			self.score += 1
			self.generatePart()
			foods[(self.head.posX, self.head.posY)].ate()
			self.foodAte = False

def renderPositions():
	global ticks
	tps = fps = frames = 0
	last_time = time.time()
	while gameNotOver:
		stdscr.clear()
		for snake in snakes:
			for part in snake.parts:
				try:
					stdscr.addch(part.posY, part.posX, part.base)
				except curses.error:
					pass
			for foodPos in foodsPos:
				try:
					stdscr.addch(foodPos[1], foodPos[0], '@')
				except curses.error:
					pass
		
		frames += 1
		current_time = time.time()
		if current_time - last_time >= 1.0:
			fps = frames
			tps = ticks
			frames = ticks = 0
			last_time = current_time
		try:
			stdscr.addstr(lines, 0, f"FPS: {fps}, TPS: {tps}")
		except curses.error:
			pass
		
		for i in range(len(snakes)):
			try:
				stdscr.addstr(f", score{i}: {snakes[i].score}, HScore: {bestScore}, episode: {Round}")
			except curses.error:
				pass
		
		stdscr.refresh()
		time.sleep(0.01)

def inputHandle():
	global gameNotOver
	key = stdscr.getch()
	if key != -1:
		if key == curses.KEY_UP and snakes[0].head.directionY != 1:
			snakes[0].head.directionY = -1
		elif key == curses.KEY_DOWN and snakes[0].head.directionY != -1:
			snakes[0].head.directionY = 1
		elif key == curses.KEY_LEFT and snakes[0].head.directionX != 1:
			snakes[0].head.directionX = -1
		elif key == curses.KEY_RIGHT and snakes[0].head.directionX != -1:
			snakes[0].head.directionX = 1
		elif key == 27:
			gameNotOver = False

replay_memory = deque(maxlen=100000)

gamma = 0.95
epsilon = 1.0
epsilon_min = 0.01
epsilon_decay = 0.995
batch_size = 64

class SnakeAI(nn.Module):
	def __init__(self):
		super(SnakeAI, self).__init__()
		self.fc1 = nn.Linear(13, 256)
		self.fc2 = nn.Linear(256, 256)
		self.fc3 = nn.Linear(256, 4)

	def forward(self, x):
		x = F.relu(self.fc1(x))
		x = F.relu(self.fc2(x))
		return self.fc3(x)

snake_ai = SnakeAI()
optimizer = optim.Adam(snake_ai.parameters(), lr=0.001)
criterion = nn.MSELoss()

def get_snake_input(snake):
	numParts = len(snake.parts) / 1000
	head = snake.head
	food = list(foods.keys())[0]
	directionX = head.directionX
	directionY = head.directionY
	dx = food[0] - head.posX
	dy = food[1] - head.posY
	
	food_ndist_x = dx / columns
	food_ndist_y = dy / lines
	food_mdist_x = dx / columns - np.sign(dx)
	food_mdist_y = dy / lines - np.sign(dy)
	
	up_ahead = ((head.posX, head.posY - 1 if head.posY != 0 else lines - 1) in partsPos)
	down_ahead = ((head.posX, head.posY + 1 if head.posY != lines - 1 else 0) in partsPos)
	left_ahead = ((head.posX - 1 if head.posX != 0 else columns - 1, head.posY) in partsPos)
	right_ahead = ((head.posX + 1 if head.posX != columns - 1 else 0, head.posY) in partsPos)
	
	input_tensor = torch.tensor([
		directionX, directionY, 
		food_ndist_x, food_ndist_y, food_mdist_x, food_mdist_y,
		up_ahead, down_ahead, left_ahead, right_ahead,
		head.posX / columns, head.posY / lines, numParts
	], dtype=torch.float32).unsqueeze(0)
	
	return input_tensor

def reset_game():
	global partsPos, foods, foodsPos, snakes
	partsPos.clear()  # Clear snake parts positions
	foods.clear()  # Clear all food objects
	foodsPos.clear()  # Clear food positions
	snakes.clear()  # Clear all snakes (if there are multiple)

def calculate_reward(snake):
	if snake.gameOver:
		return -5
	if snake.foodAte:
		return 1
	return -0.01

def train_snake_ai(model, mini_batch, optimizer, criterion, gamma):
	states, actions, rewards, next_states = zip(*mini_batch)

	states = torch.cat(states)
	actions = torch.tensor(actions).unsqueeze(1)
	rewards = torch.tensor(rewards).unsqueeze(1)
	next_states = torch.cat(next_states)

	current_q_values = model(states).gather(1, actions)

	with torch.no_grad():
		max_next_q_values = model(next_states).max(1)[0].unsqueeze(1)

	target_q_values = rewards + (gamma * max_next_q_values)

	loss = criterion(current_q_values, target_q_values)

	# Backpropagation
	optimizer.zero_grad()
	loss.backward()
	optimizer.step()

render = threading.Thread(target=renderPositions)
render.start()

prevBestScore = 0

for episode in range(250):
	Round += 1
	snake = Snake()
	Food()
	
	total_reward = 0
	game_over = False
	
	while not game_over:
		state = get_snake_input(snake)
		
		if random.random() < epsilon:
			action = random.choice([0, 1, 2, 3])
		else:
			with torch.no_grad():
				action = torch.argmax(snake_ai(state)).item()
		
		if action == 0:
			if snake.head.directionY != 1:
				snake.head.directionY = -1
		elif action == 1:
			if snake.head.directionY != -1:
				snake.head.directionY = 1
		elif action == 2:
			if snake.head.directionX != 1:
				snake.head.directionX = -1
		elif action == 3:
			if snake.head.directionX != -1:
				snake.head.directionX = 1
		
		snake.nextH()
		snake.nextP()
		if snake.foodAte:
			snake.score += 1
			if snake.score > bestScore:
				bestScore = snake.score
			snake.generatePart()
			foods[(snake.head.posX, snake.head.posY)].ate()
		
		ticks += 1
		
		next_state = get_snake_input(snake)
		reward = calculate_reward(snake)
		total_reward += reward
		
		if snake.foodAte:
			snake.foodAte = False
		
		replay_memory.append((state, action, reward, next_state))

		if snake.gameOver:
			game_over = True

		if len(replay_memory) > batch_size:
			mini_batch = random.sample(replay_memory, batch_size)
			train_snake_ai(snake_ai, mini_batch, optimizer, criterion, gamma)

		if epsilon > epsilon_min:
			epsilon *= epsilon_decay
	
	reset_game()
	if (Round + 1) % 10:
		torch.save(snake_ai.state_dict(), "snake-ai.pth")
	if bestScore > prevBestScore:
		torch.save(snake_ai.state_dict(), "high-snake-ai.pth")
		prevBestScore = bestScore

render.join()
curses.endwin()