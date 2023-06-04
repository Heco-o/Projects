const express = require('express');
const http = require('http');
const { exec } = require('child_process');
const socketIO = require('socket.io');

const app = express();
const server = http.createServer(app);
const io = socketIO(server);

// Handle incoming WebSocket connections
io.on('connection', (socket) => {
  console.log('A new client connected');

  // Execute a command in Termux
  socket.on('command', (command) => {
    exec(command, (error, stdout, stderr) => {
      // Send the command output back to the client
      socket.emit('output', stdout);
    });
  });

  // Handle disconnection
  socket.on('disconnect', () => {
    console.log('A client disconnected');
  });
});

const port = 3000;
server.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});