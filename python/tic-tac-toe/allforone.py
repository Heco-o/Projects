import json

def generate_games(positions_data):
    games = {}

    def generate_game(position, next_player):
        print("Generating game for position:", position)
        # Base case: If the position is terminal, record the outcome and return
        if position in positions_data['Xwin']:
            games[position] = 'Xwin'
            print("Found X win at position:", position)
            return
        elif position in positions_data['Owin']:
            games[position] = 'Owin'
            print("Found O win at position:", position)
            return
        elif position in positions_data['draw']:
            games[position] = 'draw'
            print("Found draw at position:", position)
            return
        elif position in positions_data['impossible']:
            games[position] = 'impossible'
            print("Found impossible position:", position)
            return

        # Recursive case: Generate all possible next moves
        next_moves = []
        for i, char in enumerate(position):
            if char == 'e':
                next_move = position[:i] + next_player + position[i+1:]
                next_moves.append(next_move)

        # Switch player for the next move
        next_player = 'x' if next_player == 'o' else 'o'

        # Recursively generate game states for each possible next move
        for move in next_moves:
            if move not in games:  # Check if the move is not already processed to avoid duplicates
                generate_game(move, next_player)

    # Iterate through each category and generate games
    for category, subcategories in positions_data.items():
        for subcategory, positions in subcategories.items():
            for position in positions:
                generate_game(position, 'x')  # Assume X starts in every position

    return games

def main():
    with open('positions.json', 'r') as f:
        positions_data = json.load(f)

    games = generate_games(positions_data)

    with open('all_possible_games.json', 'w') as f:
        json.dump(games, f, indent=4)

if __name__ == "__main__":
    main()
