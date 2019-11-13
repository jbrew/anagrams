from models.word_finder import WordFinder
from models.game import Game
from models.player import Player
from utilities.letter_distribution import distribution
from controllers.command_line import possibility_loop, plays_for_word_loop



if __name__ == '__main__':
	
	google_filter = True

	with open('resources/scrabble_dictionary.txt') as f:
		legal_words = [line.strip().upper() for line in f.readlines()]

	with open('resources/count_1w.txt') as f:
		word_freqs = [line.strip().upper().split() for line in f.readlines()]
	
	frequency_by_word = {w: int(f) for w, f in word_freqs}

	print(len(legal_words))
	
	if google_filter:
		legal_words = [w for w in legal_words if w in frequency_by_word]

	print(len(legal_words))

	wf = WordFinder(legal_words)
	
	g = Game(distribution, wf, frequency_by_word)
	
	possibility_loop(g)
	#plays_for_word_loop(g)

	



