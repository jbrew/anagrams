from models.word_finder import WordFinder
from models.game import Game
from models.player import Player
from utilities.letter_distribution import distribution
from controllers.command_line import possibility_loop, plays_for_word_loop


def binary_compounds_loop(words, wf):
	for word in words:
		compounds = wf.find_binary_compounds(word, 7)
		if len(compounds) > 0:
			print()
			print(word)
			for compound in compounds:
				print(' ' + ' '.join(compound))



if __name__ == '__main__':
	
	google_filter = True
	google_limit = 100000

	with open('resources/scrabble_dictionary.txt') as f:
		legal_words = [line.strip().upper() for line in f.readlines()]

	with open('resources/count_1w.txt') as f:
		word_freqs = [line.strip().upper().split() for line in f.readlines()][:google_limit]
	
	frequency_by_word = {w: int(f) for w, f in word_freqs}

	print('\nThere are ' + str(len(legal_words)) + ' words in the Scrabble dictionary')
	
	if google_filter:
		legal_words = [w for w in legal_words if w in frequency_by_word]

	print('...' + str(len(legal_words)) + ' of which are also in the Google corpus')

	wf = WordFinder(legal_words)
	g = Game(distribution, wf, frequency_by_word)
	
	#binary_compounds_loop(legal_words, wf)
	#possibility_loop(g)
	#plays_for_word_loop(g)

	



