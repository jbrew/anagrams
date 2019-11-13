import itertools
from word_finder import WordFinder

distribution = {
	'A': 13,
	'B': 3,
	'C': 3,
	'D': 6,
	'E': 18,
	'F': 3,
	'G': 4,
	'H': 3,
	'I': 12,
	'J': 2,
	'K': 2,
	'L': 5,
	'M': 3,
	'N': 8,
	'O': 11,
	'P': 3,
	'Q': 2,
	'R': 9,
	'S': 6,
	'T': 9,
	'U': 6,
	'V': 3,
	'W': 3,
	'X': 2,
	'Y': 3,
	'Z': 2
}


class Game(object):

	def __init__(self, distribution, word_finder):
		
		self.all_letters = distribution
		self.letter_pool = []

		self.player_words = {}		# format {'name': ['listed', 'words']}
		
		self.wf = word_finder

	def reveal_letter(self):
		pass

	# plays that can be made by combining any of the given letters
	# with any of the given words
	def available_plays(self, letters, words=[]):
		key_for_all_letters = self.wf.anagram_key_for_letters(letters)
		combo_keys = self.wf.factor_tree_descendants(key_for_all_letters)
		plays = []
		for word in words:
			plays.extend(self.plays_for_word_and_combos(word, combo_keys))
		return plays

	def plays_for_word_and_combos(self, word, letter_combo_keys):
		word_key = self.wf.anagram_key_for_letters(word)

		plays = []
		for combo_key in letter_combo_keys:
			combo_letters = self.wf.letters_for_anagram_key(combo_key)
			product = word_key * combo_key
			if product in self.wf.anagram_dict:
				plays_using_letters = list(self.wf.anagram_dict[product])
				valid_plays = [p for p in plays_using_letters if len(p) > len(word)]
				if len(valid_plays) > 0:
					plays.append({'base': word, 'additions': combo_letters, 'results': valid_plays})

		return plays

	def string_for_distribution(self, distribution):
		return ''.join([''.join([k for i in range(v)]) for k, v in distribution.items()])

	# plays that would be possible by revealing some number of letters
	def possibilities(self, word, num_letters_added=1):
		letter_pool = self.string_for_distribution(self.all_letters)
		combos = self.wf.combos_from_n_blanks(num_letters_added)
		combo_keys = [self.wf.anagram_key_for_letters(c) for c in combos]
		return sorted(self.plays_for_word_and_combos(word, combo_keys), key=lambda x: len(x['additions']))

### PLAYERS ###


class Player(object):

	def __init__(self, name):
		self.name = name
		self.words = []



### UI SUGAR ###

def play_string(play):
	return "{} + {} --> {}".format(	play['base'],
									play['additions'],
									' or '.join(play['results']))


### TESTS ####


def available_plays_test(game):
	for play in game.available_plays(letters='ABCDE', words=['HELLO','RACHEL']):
		print(play_string(play))

def possibility_demo(game):
	print()
	for play in g.possibilities('HEATED', 2):
		print(play_string(play))


def plays_for_word_loop(game):
	while True:
		word, letters = input('Enter word and letter pool:\n').upper().split(' ')
		key_for_letters = game.wf.anagram_key_for_letters(letters)
		combo_keys = game.wf.factor_tree_descendants(key_for_letters)

		for play in game.plays_for_word_and_combos(word, combo_keys):
			print(play_string(play))


if __name__ == '__main__':
	with open('scrabble_dictionary.txt') as f:
		legal_words = [line.strip().upper() for line in f.readlines()]

	with open('count_1w.txt') as f:
		word_rates = [line.strip().upper().split() for line in f.readlines()]


	wf = WordFinder(legal_words)

	g = Game(distribution, wf)
	#available_plays_test(g)
	possibility_demo(g)
	#plays_for_word_loop(g)

	



