


def available_plays_test(game):
	for play in game.available_plays(letters='ABCDETNAPE', words=['HELLO','DARKNESS']):
		print(string_for_play(play))
