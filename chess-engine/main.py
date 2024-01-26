import asyncio
import chess.engine
import chess.pgn

async def __play_game(engine1_path, engine2_path, pgn=False):
	_, engine1 = await chess.engine.popen_uci(engine1_path)
	_, engine2 = await chess.engine.popen_uci(engine2_path)
	
	if pgn:
		game = chess.pgn.Game()
		game.headers["Event"] = ""
		game.headers["Site"] = ""
		game.headers["Date"] = ""
		game.headers["Round"] = ""
		game.headers["White"] = ""
		game.headers["Black"] = ""
	
	
	board = chess.Board()
	result = await engine1.play(board, chess.engine.Limit(time=0.1))
	if pgn:
		node = game.add_variation(result.move)
		board.push(result.move)
	
	
	while not board.is_game_over():
		if board.turn == chess.BLACK:
			result = await engine2.play(board, chess.engine.Limit(nodes=1), ponder=True)
		else:
			result = await engine1.play(board, chess.engine.Limit(nodes=1), ponder=True)
		
		if pgn:
			node = node.add_variation(result.move)
		
		board.push(result.move)
		print("\n", board, sep="")
	
	print("Game Over. Result: " + board.result())
	
	
	await engine1.quit()
	await engine2.quit()
	
	if pgn:
		game.headers["Result"] = board.result()
		print(game)
		with open("/storage/emulated/0/DroidFish/pgn/Tgame.pgn", "w") as File:
			File.write(str(game))

def play(engine1_path, engine2_path, pgn=False):
	loop = asyncio.get_event_loop()
	loop.run_until_complete(__play_game(engine1_path, engine2_path, pgn))

if __name__ == "__main__":
	engine1_path = "/data/data/com.termux/files/home/github/Projects/chess-engine/velvet-v5-3"
	engine2_path = "/data/data/com.termux/files/home/github/Projects/chess-engine/velvet-v4"
	
	play(engine1_path, engine2_path, True)