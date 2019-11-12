# find all primes up to a limit
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

def words_formable_from_letters(letters, prime_anagram_dict, lookup, num_blanks=0):
	key = get_prime_anagram_key(letters, lookup)
	primes=list(lookup.values())
	factor_tree_nodes = get_factor_tree_nodes(key, lookup, primes, num_blanks=num_blanks)

	formable_words = []
	for node in factor_tree_nodes:
		if node in prime_anagram_dict:
			formable_words.extend(prime_anagram_dict[node])
	return sorted(formable_words, key=len)

def blank_permutations(num_blanks, alphabet='abcdefghijklmnopqrstuvwxyz'):
	if num_blanks == 1:
		return list(alphabet)
	else:
		permutations = list(alphabet)
		for i, letter in enumerate(alphabet):
			permutations.extend([letter + p for p in blank_permutations(num_blanks-1, alphabet[i:])])
		return permutations

def get_factor_tree_nodes(key, lookup, primes, num_blanks=0):

	blank_sets_to_add = blank_permutations(num_blanks)

	factor_tree_nodes = factorize(key, primes)
	#print(factor_tree_nodes)
	
	for blank_values in blank_sets_to_add:
		print(blank_values)
		product = 1
		for letter in blank_values:
			prime_factor = lookup[letter]
			primes_subset = [p for p in primes if not p==prime_factor]
			product *= prime_factor
		factor_tree_nodes.extend(factorize(key*product, primes_subset))
	return factor_tree_nodes

if __name__ == '__main__':
	with open('scrabble_dictionary.txt') as f:
		words = [line.strip().lower() for line in f.readlines()]

	d, lookup = build_prime_anagram_dictionary(words)
	primes = sieve_of_eratosthenes(1000)[:26]

	#print(factorize(126, primes))
	#print(words_formable_from_letters('carthorse', d, lookup))

	#print(blank_permutations(2, alphabet='abcd'))
	#print(blank_permutations(3, alphabet='abcd'))

	print(words_formable_from_letters('taxi', d, lookup, num_blanks=2))



