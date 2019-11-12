

class Board(object):
	
	def __init__(self, num_rows, num_cols):
		self.squares = [['.' for c in range(num_cols)] for r in range(num_rows)]

	def to_string(self):
		return '\n'.join([' '.join(row) for row in self.squares])

	# modifies board in place
	def place_tile(self, x, y, letter):
		self.square[x][y] = letter


class Game(object):

	def __init__(self, board_size=15):
		self.board = Board(board_size, board_size)


if __name__ == '__main__':
	b = Board(5, 5)
	print(b.to_string())

