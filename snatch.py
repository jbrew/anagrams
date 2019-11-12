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
		self.players = []
		self.hidden_letters = distribution
		self.available_letters = []

		self.wf = word_finder

	def reveal_letter(self):
		pass

	# plays that can be made from letters on the board right now
	def available_plays(self, letters, words=[]):

		# find keys for all combinations of letters in the central pool
		key_for_all_letters = self.wf.anagram_key_for_letters(letters)
		combo_keys = self.wf.factor_tree_descendants(key_for_all_letters)
	
		# find anagram key for each word (product of letters)
		word_keys = [self.wf.anagram_key_for_letters(word) for word in words]

		plays = []

		# for each letter combination, find words formable by adding one word
		# TODO: one word or more
		for combo_key in combo_keys:
			combo_letters = self.wf.letters_for_anagram_key(combo_key)

			for word in words:
				word_key = self.wf.anagram_key_for_letters(word)
				product = combo_key*word_key

				if product in wf.anagram_dict:
					
					plays_using_word = wf.anagram_dict[product]
					valid_plays = [p for p in list(plays_using_word) if len(p) > len(word)]

					if len(valid_plays) > 0:
						plays.append((word, combo_letters, valid_plays))

		return plays



	# plays that would be possible by revealing some number of letters
	def possible_plays(self, num_letters_to_reveal):
		pass


class Player(object):

	def __init__(self, name):
		self.name = name
		self.words = []





if __name__ == '__main__':
	with open('scrabble_dictionary.txt') as f:
		legal_words = [line.strip().upper() for line in f.readlines()]
	wf = WordFinder(legal_words)

	g = Game(distribution, wf)
	plays = g.available_plays(letters='ABCDE', words=['DEATH','HELLO'])

	for p in plays:
		print(p)
	

