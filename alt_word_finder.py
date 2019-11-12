#### ALTERNATE IMPLEMENTATION AS TWO SEPARATE FUNCTIONS ###

# returns all unique anagram_keys contained within the given key
def subkeys_for_anagram_key(anagram_key):
	subkeys_found = [anagram_key]
	current_step = [anagram_key]
	while len(current_step) > 0:
		next_step = set([])
		for key in current_step:
			immediate_subkeys = get_deletes(key)
			next_step = next_step.union(set(immediate_subkeys))
		current_step = list(next_step)
		subkeys_found.extend(current_step)
	return subkeys_found

# first get all subkeys, then combine all their associated words
def alt_words_formable_from(letters, anagram_dictionary):
	formable_words = []
	for subkey in subkeys_for_anagram_key(get_anagram_key(letters)):
		if subkey in anagram_dictionary:
			formable_words.extend(list(anagram_dictionary[subkey]))
	return formable_words
