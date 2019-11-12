

# find all primes up to a given limit
def sieve_of_eratosthenes(limit):	
	import math
	primes = [True for x in range(limit)]
	primes[0] = False
	primes[1] = False
	for n in range(math.floor(limit/2)):
		if primes[n]:
			for i in range(2*n, limit, n):
				primes[i] = False
	return [i for i, p in enumerate(primes) if p]

def build_prime_anagram_dictionary(words):
	alphabet = 'abcdefghijklmnopqrstuvwxyz'
	primes = sieve_of_eratosthenes(1000)
	lookup = {alphabet[i]: primes[i] for i in range(len(alphabet))}
	d = {}
	for word in words:
		key = get_prime_anagram_key(word, lookup)		
		if key in d:
			d[key].add(word)
		else:
			d[key] = set([word])
	return d, lookup

def get_prime_anagram_key(word, lookup):
	product = 1
	for letter in word:
		product *= lookup[letter]
	return product

def factorize(n, primes, first_to_check=0):
	factor_tree_nodes = [n]
	index = first_to_check
	while index < len(primes):
		if n % primes[index] == 0:
			result = n // primes[index]
			factor_tree_nodes.extend(factorize(result, primes, first_to_check=index))
		index += 1
	return factor_tree_nodes

def words_formable_from_letters_prime(letters, prime_anagram_dict, lookup, num_blanks=0):
	key = get_prime_anagram_key(letters, lookup)
	primes=list(lookup.values())


	factor_tree_nodes = factor_tree_nodes_n_blanks(key, lookup, primes, num_blanks=num_blanks)

	# handle blanks
	#for i in range(num_blanks):
	#	factor_tree_nodes = expand_with_blank_prime(factor_tree_nodes, lookup)

	formable_words = []
	for node in factor_tree_nodes:
		if node in prime_anagram_dict:
			formable_words.extend(prime_anagram_dict[node])
	return sorted(formable_words, key=len)

def expand_with_blank_prime(factor_tree_nodes, lookup):
	expanded = []
	alphabet = 'abcdefghijklmnopqrstuvwxyz'
	for node in factor_tree_nodes:
		for letter in alphabet:
			prime_factor = lookup[letter]
			expanded.append(node)
			expanded.append(node * prime_factor)
	return expanded

def factor_tree_nodes_one_blank(key, lookup, primes):
	factor_tree_nodes = factorize(key, primes)
	alphabet = 'abcdefghijklmnopqrstuvwxyz'
	for letter in alphabet:
		prime_factor = lookup[letter]
		primes_subset = [p for p in primes if not p==prime_factor]
		factor_tree_nodes.extend(factorize(key*prime_factor, primes_subset))
	return factor_tree_nodes


def factor_tree_nodes_n_blanks(key, lookup, primes, num_blanks=0):
	if num_blanks == 0:
		return factorize(key, primes)
	else:
		factor_tree_nodes = []
		alphabet = 'abcdefghijklmnopqrstuvwxyz'
		for letter in alphabet:
			prime_factor = lookup[letter]
			primes_subset = [p for p in primes if not p==prime_factor]
			factor_tree_nodes.extend(factor_tree_nodes_n_blanks(key*prime_factor, lookup, primes_subset, num_blanks-1))
		return factor_tree_nodes


def anagrams_for_word(word, prime_anagram_dict, lookup):
	key = get_prime_anagram_key(word, lookup)
	print(key)
	return prime_anagram_dict[key]

# a dictionary of words in which each key is a unique sorted list of letters, or "anagram key"
def build_anagram_dictionary(words):
	d = {}
	for word in words:
		ak = get_anagram_key(word)
		if ak in d:
			d[ak].add(word)
		else:
			d[ak] = set([word])
	return d

# generate key by sorting letters in a given string
def get_anagram_key(letters):
	return ''.join(sorted(letters))

# all words formable by any subset of the given letters
def words_formable_from_letters(letters, anagram_dictionary, num_blanks=0):
	formable_words = []
	current_step = [get_anagram_key(letters)]

	# optional: consider all initial letter sets attainable by adding wildcards
	# if num_blanks is 0, this does nothing
	current_step = expand_with_blanks(current_step, num_blanks)

	while len(current_step) > 0:
		next_step = []
		for key in current_step:
			if key in anagram_dictionary:
				formable_words.extend(list(anagram_dictionary[key]))
			next_step.extend(get_deletes(key))
		current_step = list(set(next_step))		# eliminate duplicates

	return list(reversed([word + " " + str(len(word)) for word in formable_words]))

# all keys attainable by removing one letter from an anagram key
def get_deletes(anagram_key):
	return [anagram_key[:i] + anagram_key[i+1:] for i in range(len(anagram_key))]

def expand_with_blanks(current_step, num_blanks):
	for i in range(num_blanks):		# expand num_blanks times
		next_step = []
		for letter_set in current_step:
			next_step.extend(get_insertions(letter_set))
		current_step = list(set(next_step))
	return current_step

# all keys attainable by adding one letter into the mix
# called when handling blanks
def get_insertions(anagram_key):
	alphabet = 'abcdefghijklmnopqrstuvwxyz'
	return [''.join(sorted(anagram_key + c)) for c in alphabet]

### TIME TESTING ###

import time
def solve_all_letter_sets(letter_sets, ad):
	start = time.time()
	for i, letter_set in enumerate(letter_sets):
		formable_words = words_formable_from_letters(letter_set, ad)
		
		if (i+1) % 1000 == 0:
			time_taken = time.time() - start
			print('completed {} letter sets in {} seconds'.format(i+1, time_taken))



### UI ###

def user_loop():

	with open('scrabble_dictionary.txt') as f:
		words = [line.strip().lower() for line in f.readlines()]

	anagram_dict = build_anagram_dictionary(words)

	while True:
		user_input = input('Enter letters:\n')
		letters = ''.join([c for c in user_input if not c=='?'])
		num_blanks = len([c for c in user_input if c=='?'])
		print('\t\t'.join(words_formable_from_letters(letters, anagram_dict, num_blanks)))



if __name__ == '__main__':
	with open('scrabble_dictionary.txt') as f:
		words = [line.strip().lower() for line in f.readlines()]

	d, lookup = build_prime_anagram_dictionary(words)
	print(anagrams_for_word('carthorse', d, lookup))

	primes = sieve_of_eratosthenes(1000)[:26]
	print(factorize(126, primes))

	#print(words_formable_from_letters_prime('carthorse', d, lookup))

	print(words_formable_from_letters_prime('taxi', d, lookup, num_blanks=1))	

	#print(sieve_of_eratosthenes(100))

	#user_loop()





### TESTS ###

def various_tests():
	with open('scrabble_dictionary.txt') as f:
		words = [line.strip().lower() for line in f.readlines()]

	anagram_dict = build_anagram_dictionary(words)
	print(get_anagram_key('jamal'))
	#print(words_formable_from_letters('thatched', anagram_dict))
	print(words_formable_from_letters('jamal', anagram_dict))
	#print(subkeys_for_anagram_key(get_anagram_key('thatched')))
	print(words_formable_from_letters('waouxns', anagram_dict, num_blanks=1))
	print(words_formable_from_letters('rachosetr', anagram_dict, num_blanks=0))
	print(words_formable_from_letters('srecureiv', anagram_dict, num_blanks=0))
	print(words_formable_from_letters('aiedane', anagram_dict, num_blanks=0))



