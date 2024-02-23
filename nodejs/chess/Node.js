const express = require('express');
const path = require('path');
const { spawn } = require('child_process');

const app = express();
const port = 3000;

// Serve static files
app.use(express.static(path.join(__dirname, 'public')));

// Path to the Stockfish binary
const stockfishPath = path.join(__dirname, 'stockfish');

// Start Stockfish engine process
const stockfish = spawn(stockfishPath);

// Handle Stockfish output
stockfish.stdout.on('data', (data) => {
    console.log(`Stockfish output: ${data}`);
});

stockfish.stderr.on('data', (data) => {
    console.error(`Stockfish error: ${data}`);
});

// Start HTTP server
app.get('/bestMove', (req, res) => {
    const fen = req.query.fen;
    const input = `position fen ${fen}\ngo depth 15\n`;

    stockfish.stdin.write(input);
    stockfish.stdin.end();

    let bestMove = '';

    stockfish.stdout.on('data', (data) => {
        const lines = data.toString().split('\n');
        for (const line of lines) {
            if (line.startsWith('bestmove')) {
                bestMove = line.split(' ')[1];
                break;
            }
        }
        res.json({ bestMove });
    });
});

app.listen(port, () => {
    console.log(`Server is running at http://localhost:${port}`);
});
