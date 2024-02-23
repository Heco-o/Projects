const express = require('express');
const http = require('http');
const {
	spawn
} = require('child_process');
const socketIO = require('socket.io');
const path = require('path');

const app = express();
const server = http.createServer(app);
const io = socketIO(server);

// Serve static files from the "public" directory
app.use(express.static(path.join(__dirname, 'public')));

// Handle incoming WebSocket connections
io.on('connection', (socket) => {
	console.log('A new client connected');

	// Create a new terminal session
	const term = spawn('bash');

	// Send terminal output to the client
	term.stdout.on('data', (data) => {
		socket.emit('output', data.toString());
	});

	// Send terminal errors to the client
	term.stderr.on('data', (data) => {
		socket.emit('error', data.toString());
	});

	// Execute commands in the terminal
	socket.on('command', (command) => {
		term.stdin.write(command + '\n');
	});

	// Handle disconnection
	socket.on('disconnect', () => {
		console.log('A client disconnected');
		term.kill();
	});
});

const port = 3000;
server.listen(port, () => {
	console.log(`Server is running on port ${port}`);
});
