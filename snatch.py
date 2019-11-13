import itertools
from word_finder import WordFinder

# How many of each bananagram tile there are
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

def string_for_distribution(distribution):
	"""
	Represent letter distribution as a big old string
	"""
	return ''.join([''.join([k for i in range(v)]) for k, v in distribution.items()])

### UI SUGAR ###

def string_for_play(play):
	return "{} + {} --> {}".format(	play['base'],
									play['additions'],
									' or '.join(play['results']))

class Game(object):

	def __init__(self, distribution, word_finder):
		
		self.all_letters = distribution
		self.letter_pool = []

		self.player_words = {}		# format {'name': ['listed', 'words']}
		
		self.wf = word_finder

	def reveal_letter(self):
		pass

	
	def available_plays(self, letters, words=[]):
		"""
		Plays that can be made by combining any of the given letters
		with any of the given words.
		"""
		key_for_all_letters = self.wf.anagram_key_for_letters(letters)
		combo_keys = self.wf.factor_tree_descendants(key_for_all_letters)
		plays = []
		for word in words:
			plays.extend(self.plays_for_word_and_combos(word, combo_keys))
		return plays

	def plays_for_word_and_combos(self, word, letter_combo_keys):
		"""
		Given a word and a list of keys corresponding to unique letter
		combinations that could be added to it, find all plays that can
		be made using the whole word and the whole of any of the combos.
		"""
		word_key = self.wf.anagram_key_for_letters(word)
		plays = []
		for combo_key in letter_combo_keys:
			product = word_key * combo_key
			if product in self.wf.anagram_dict:
				plays_using_letters = list(self.wf.anagram_dict[product])
				valid_plays = [p for p in plays_using_letters if len(p) > len(word)]
				if len(valid_plays) > 0:
					difference = self.difference_between_words(word, valid_plays[0])
					plays.append({'base': word, 'additions': difference, 'results': valid_plays})

		return plays

	def difference_between_words(self, small, big):
		"""
		Return the letters that must be added to a smaller word
		to make a bigger word.

		Maybe we can do this more elegantly with primes.
		"""
		small, big = list(small), list(big)
		while len(small) > 0:
			big.remove(small[0])
			small.pop(0)
		return ''.join(big)

	def possibilities(self, word, num_letters_added=1):
		"""
		
		Find plays that would be possible with some number of
		added letters. This problem is nearly equivalent to a scrabble
		hand with blanks.

		TODO: Calculate possibilities based on actual remaining distribution,
		rather than treating each blank as a total wildcard.

		"""
		letter_pool = string_for_distribution(self.all_letters)
		combos = self.wf.combos_from_n_blanks(num_letters_added)
		combo_keys = [self.wf.anagram_key_for_letters(c) for c in combos]

		# sort by ascending length
		return sorted(self.plays_for_word_and_combos(word, combo_keys), key=lambda x: len(x['additions']))


### PLAYERS ###

class Player(object):

	def __init__(self, name):
		self.name = name
		self.words = []


### TESTS AND DEMOS ####

def available_plays_test(game):
	for play in game.available_plays(letters='ABCDETNAPE', words=['HELLO','DARKNESS']):
		print(string_for_play(play))

def possibility_loop(game):
	while True:
		user_input = input('Enter a word:\n')
		args = user_input.strip().split()

		if not len(args) in [1,2]:
			print('Please enter either:\n\t> [word]\n...or:\n> [word] [# of blanks]')
			continue

		if len(args) == 1:
			letters = ''.join([c for c in args[0] if not c=='?']).upper()
			num_blanks = len([c for c in args[0] if c=='?'])
			plays = game.possibilities(letters, num_blanks)
		elif len(args) == 2:
			letters = args[0]
			num_blanks = args[1]
			plays = game.possibilities(letters, num_blanks)
		
		for play in plays:
			print(string_for_play(play))


def plays_for_word_loop(game):
	while True:
		word, letters = input('Enter word and letter pool:\n').upper().split(' ')
		key_for_letters = game.wf.anagram_key_for_letters(letters)
		combo_keys = game.wf.factor_tree_descendants(key_for_letters)

		for play in game.plays_for_word_and_combos(word, combo_keys):
			print(string_for_play(play))


if __name__ == '__main__':
	with open('scrabble_dictionary.txt') as f:
		legal_words = [line.strip().upper() for line in f.readlines()]

	with open('count_1w.txt') as f:
		word_rates = [line.strip().upper().split() for line in f.readlines()]


	wf = WordFinder(legal_words)
	g = Game(distribution, wf)
	available_plays_test(g)
	possibility_loop(g)
	#plays_for_word_loop(g)

	



