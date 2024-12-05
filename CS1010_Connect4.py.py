import numpy as np
import random
import pygame
import sys
import math

blue = (0,0,255)
black = (0,0,0)
red = (255,0,0)
yellow = (255,255,0)

row_count = 6
column_count = 7

player = 0
ai = 1

empty = 0
player_piece = 1
ai_piece = 2

window_length = 4

def create_board():
	board = np.zeros((row_count,column_count))
	return board

def drop_piece(board, row, col, piece):
	board[row][col] = piece

def is_valid_location(board, col):
	return board[row_count-1][col] == 0

def get_next_open_row(board, col):
	for r in range(row_count):
		if board[r][col] == 0:
			return r

def print_board(board):
	print(np.flip(board, 0))

def winning_move(board, piece):
	# check horizontal locations for win
	for c in range(column_count-3):
		for r in range(row_count):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return true

	# check vertical locations for win
	for c in range(column_count):
		for r in range(row_count-3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return true

	# check positively sloped diaganols
	for c in range(column_count-3):
		for r in range(row_count-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return true

	# check negatively sloped diaganols
	for c in range(column_count-3):
		for r in range(3, row_count):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return true

def evaluate_window(window, piece):
	score = 0
	opp_piece = player_piece
	if piece == player_piece:
		opp_piece = ai_piece

	if window.count(piece) == 4:
		score += 100
	elif window.count(piece) == 3 and window.count(empty) == 1:
		score += 5
	elif window.count(piece) == 2 and window.count(empty) == 2:
		score += 2

	if window.count(opp_piece) == 3 and window.count(empty) == 1:
		score -= 4

	return score

def score_position(board, piece):
	score = 0

	## score center column
	center_array = [int(i) for i in list(board[:, column_count//2])]
	center_count = center_array.count(piece)
	score += center_count * 3

	## score horizontal
	for r in range(row_count):
		row_array = [int(i) for i in list(board[r,:])]
		for c in range(column_count-3):
			window = row_array[c:c+window_length]
			score += evaluate_window(window, piece)

	## score vertical
	for c in range(column_count):
		col_array = [int(i) for i in list(board[:,c])]
		for r in range(row_count-3):
			window = col_array[r:r+window_length]
			score += evaluate_window(window, piece)

	## score posiive sloped diagonal
	for r in range(row_count-3):
		for c in range(column_count-3):
			window = [board[r+i][c+i] for i in range(window_length)]
			score += evaluate_window(window, piece)

	for r in range(row_count-3):
		for c in range(column_count-3):
			window = [board[r+3-i][c+i] for i in range(window_length)]
			score += evaluate_window(window, piece)

	return score

def is_terminal_node(board):
	return winning_move(board, player_piece) or winning_move(board, ai_piece) or len(get_valid_locations(board)) == 0

def minimax(board, depth, alpha, beta, maximizingplayer):
	valid_locations = get_valid_locations(board)
	is_terminal = is_terminal_node(board)
	if depth == 0 or is_terminal:
		if is_terminal:
			if winning_move(board, ai_piece):
				return (none, 100000000000000)
			elif winning_move(board, player_piece):
				return (none, -10000000000000)
			else: # game is over, no more valid moves
				return (none, 0)
		else: # depth is zero
			return (none, score_position(board, ai_piece))
	if maximizingplayer:
		value = -math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, ai_piece)
			new_score = minimax(b_copy, depth-1, alpha, beta, false)[1]
			if new_score > value:
				value = new_score
				column = col
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return column, value

	else: # minimizing player
		value = math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, player_piece)
			new_score = minimax(b_copy, depth-1, alpha, beta, true)[1]
			if new_score < value:
				value = new_score
				column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return column, value

def get_valid_locations(board):
	valid_locations = []
	for col in range(column_count):
		if is_valid_location(board, col):
			valid_locations.append(col)
	return valid_locations

def pick_best_move(board, piece):

	valid_locations = get_valid_locations(board)
	best_score = -10000
	best_col = random.choice(valid_locations)
	for col in valid_locations:
		row = get_next_open_row(board, col)
		temp_board = board.copy()
		drop_piece(temp_board, row, col, piece)
		score = score_position(temp_board, piece)
		if score > best_score:
			best_score = score
			best_col = col

	return best_col

def draw_board(board):
	for c in range(column_count):
		for r in range(row_count):
			pygame.draw.rect(screen, blue, (c*squaresize, r*squaresize+squaresize, squaresize, squaresize))
			pygame.draw.circle(screen, black, (int(c*squaresize+squaresize/2), int(r*squaresize+squaresize+squaresize/2)), radius)
	
	for c in range(column_count):
		for r in range(row_count):		
			if board[r][c] == player_piece:
				pygame.draw.circle(screen, red, (int(c*squaresize+squaresize/2), height-int(r*squaresize+squaresize/2)), radius)
			elif board[r][c] == ai_piece: 
				pygame.draw.circle(screen, yellow, (int(c*squaresize+squaresize/2), height-int(r*squaresize+squaresize/2)), radius)
	pygame.display.update()

board = create_board()
print_board(board)
game_over = false

pygame.init()

squaresize = 100

width = column_count * squaresize
height = (row_count+1) * squaresize

size = (width, height)

radius = int(squaresize/2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.sysfont("monospace", 75)

turn = random.randint(player, ai)

while not game_over:

	for event in pygame.event.get():
		if event.type == pygame.quit:
			sys.exit()

		if event.type == pygame.mousemotion:
			pygame.draw.rect(screen, black, (0,0, width, squaresize))
			posx = event.pos[0]
			if turn == player:
				pygame.draw.circle(screen, red, (posx, int(squaresize/2)), radius)

		pygame.display.update()

		if event.type == pygame.mousebuttondown:
			pygame.draw.rect(screen, black, (0,0, width, squaresize))
			#print(event.pos)
			# ask for player 1 input
			if turn == player:
				posx = event.pos[0]
				col = int(math.floor(posx/squaresize))

				if is_valid_location(board, col):
					row = get_next_open_row(board, col)
					drop_piece(board, row, col, player_piece)

					if winning_move(board, player_piece):
						label = myfont.render("player 1 wins!!", 1, red)
						screen.blit(label, (40,10))
						game_over = true

					turn += 1
					turn = turn % 2

					print_board(board)
					draw_board(board)


	# # ask for player 2 input
	if turn == ai and not game_over:				

		#col = random.randint(0, column_count-1)
		#col = pick_best_move(board, ai_piece)
		col, minimax_score = minimax(board, 5, -math.inf, math.inf, true)

		if is_valid_location(board, col):
			#pygame.time.wait(500)
			row = get_next_open_row(board, col)
			drop_piece(board, row, col, ai_piece)

			if winning_move(board, ai_piece):
				label = myfont.render("player 2 wins!!", 1, yellow)
				screen.blit(label, (40,10))
				game_over = true

			print_board(board)
			draw_board(board)

			turn += 1
			turn = turn % 2

	if game_over:
		pygame.time.wait(3000)

