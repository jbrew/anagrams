


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
					difference = self.wf.difference_between_words(word, valid_plays[0])
					plays.append({'base': word, 'additions': difference, 'results': valid_plays})

		return plays

	def possibilities(self, word, num_letters_added=1):
		"""
		
		Find plays that would be possible with some number of
		added letters. This problem is nearly equivalent to a scrabble
		hand with blanks.

		TODO: Calculate possibilities based on actual remaining distribution,
		rather than treating each blank as a total wildcard.
		#letter_pool = string_for_distribution(self.all_letters)

		"""
		combos = self.wf.combos_from_n_blanks(num_letters_added)
		combo_keys = [self.wf.anagram_key_for_letters(c) for c in combos]

		# sort by ascending length, then by frequency in the google corpus
		return sorted(self.plays_for_word_and_combos(word, combo_keys),
													 key=lambda x: (len(x['additions']), self.wf.frequency(x['results'][0])))




