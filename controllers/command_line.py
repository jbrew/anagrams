
def possibility_loop(game):
	print()
	while True:
		user_input = input('Enter a word and some question marks representing blanks:\n')
		args = user_input.strip().split()

		if not len(args) in [1,2]:
			print('Please enter either:\n> [word]\n...or:\n> [word] [# of blanks]')
			continue

		if len(args) == 1:
			letters = ''.join([c for c in args[0] if not c=='?']).upper()
			num_blanks = len([c for c in args[0] if c=='?'])
			plays = game.possibilities(letters, num_blanks)
		elif len(args) == 2:
			letters = args[0].upper()
			num_blanks = int(args[1])
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

def string_for_play(play):
	return "{} + {} --> {}".format(	play['base'],
									play['additions'],
									' or '.join(play['results']))


