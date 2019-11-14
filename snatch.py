from models.word_finder import WordFinder
from models.game import Game
from models.player import Player
from utilities.letter_distribution import distribution
from controllers.command_line import possibility_loop, plays_for_word_loop

import random

def binary_compounds_loop(wf):
	for word in wf.words:
		compounds = wf.find_binary_compounds(word, 7)
		if len(compounds) > 0:
			print()
			print(word)
			for compound in compounds:
				print(' ' + ' '.join(compound))

def snowball_test(wf, words_to_check=5000):

	highlights = []
	for word in legal_words[:words_to_check]:
		snowball_paths = wf.snowball_paths_for_word(word)
		longest_path = max(snowball_paths, key=len)
		highlights.append(longest_path)
	highlights = sorted(highlights, key=len, reverse=True)

	print()
	print('longest paths overall')
	for path in highlights[:300]:
		print()
		wf.pretty_print_path(path)

if __name__ == '__main__':
	
	google_limit = 55000
	google_filter = True

	with open('resources/scrabble_dictionary.txt') as f:
		legal_words = [line.strip().upper() for line in f.readlines()]

	with open('resources/count_1w.txt') as f:
		word_freqs = [line.strip().upper().split() for line in f.readlines()][:google_limit]

	frequency_by_word = {w: int(f) for w, f in word_freqs}

	if google_filter:
		legal_words = [w for w in legal_words if w in frequency_by_word]

	print('\nThere are ' + str(len(legal_words)) + ' words in the Scrabble dictionary')
	print('...' + str(len(legal_words)) + ' of which are also in the Google corpus')

	wf = WordFinder(legal_words, frequency_by_word)
	g = Game(distribution, wf)
	
	snowball_test(wf, words_to_check=2000)
	#binary_compounds_loop(wf)
	#possibility_loop(g)
	#plays_for_word_loop(g)

	



