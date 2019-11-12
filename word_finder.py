import math


# finds all primes up to a limit
def sieve_of_eratosthenes(limit):
	primes = [True for x in range(limit)]
	primes[0] = False    # 0 is not prime
	primes[1] = False    # 1 is not prime
	for n in range(math.floor(limit/2)):
		if primes[n]:
			for i in range(2*n, limit, n):
				primes[i] = False
	return [i for i, p in enumerate(primes) if p]

# takes an alphabet and a list of primes at least as long as the alphabet
def letters_to_primes_lookup(primes, alphabet='abcdefghijklmnopqrstuvwxyz'):
	return {alphabet[i]: primes[i] for i in range(len(alphabet))}


class WordFinder(object):

	def __init__(self, words):
		
		self.primes = sieve_of_eratosthenes(1000)[:26]			# 26 primes for the 26 letters of the alphabet
		self.lookup = letters_to_primes_lookup(self.primes)
		self.anagram_dict = self.build_anagram_dictionary(words)

	def anagram_key_for_word(self, word):
		"""
		Multiply together the primes associated with each letter of the word.
		Words containing the same set of letters will yield the same product.
		"""
		product = 1
		for letter in word:
			product *= self.lookup[letter]
		return product

	def build_anagram_dictionary(self, words):
		"""
		Build a dictionary where each key is the unique hash for a letter set
		and each value is the set of words using all its letters.
		"""
		d = {}
		for word in words:
			key = self.anagram_key_for_word(word)		
			if key in d:
				d[key].add(word)
			else:
				d[key] = set([word])
		return d

	def factor_tree_descendants(self, n, primes, start_index=0):
		"""
		Returns a list of keys at all nodes in the factor tree with n
		as the root by trying to divide by all primes in the list
		after a given start_index.

		We move the start index at each level to ensure that we only
		report each node once.

		Example: If the given key is 150, we could reach the node
		at 10 by two paths: by dividing by 3 then 5, OR 5 then 3. 
		
		We avoid this by only checking primes that are equal to or greater
		than the highest prime checked in the current branch. In our example,
		once we have divided 150 by 5 to get 30, we move that branch's start
		index to 5, so we won't try dividing by 3.
		"""
		factor_tree_nodes = [n]
		index = start_index
		while index < len(primes):
			if n % primes[index] == 0:
				result = n // primes[index]
				factor_tree_nodes.extend(self.factor_tree_descendants(result, primes, start_index=index))
			index += 1
		return factor_tree_nodes

	def words_formable_from_letters(self, letters, num_blanks=0):
		"""
		Find all words formable with any subset of the given letters
		and up to [num_blanks] blank wildcards.
		"""
		key = self.anagram_key_for_word(letters)
		primes=list(self.lookup.values())
		factor_tree_nodes = self.get_factor_tree_nodes(key, num_blanks=num_blanks)

		formable_words = []
		for node in factor_tree_nodes:
			if node in self.anagram_dict:
				formable_words.extend(self.anagram_dict[node])
		return sorted(formable_words, key=len)

	def combos_from_n_blanks(self, num_blanks, alphabet='abcdefghijklmnopqrstuvwxyz'):
		"""
		Given a number of blanks, finds all unique combinations
		of n (or fewer) letters from an alphabet.
		"""
		if num_blanks == 0:
			return []
		else:
			permutations = list(alphabet)
			for i, letter in enumerate(alphabet):
				permutations.extend([letter + p for p in self.combos_from_n_blanks(num_blanks-1, alphabet[i:])])
			return permutations

	def get_factor_tree_nodes(self, key, num_blanks=0):
		"""
		Given a key representing a letter set, find keys for all unique
		letter sets formable by removing any number of letters and 
		adding up to [num_blanks] letters.

		# Note on handling blanks

		When adding a letter to the letter set, we want to find all the letter
		sets it enables, but we need to AVOID duplicating any of the
		letter sets that were already possible WITHOUT the blank.

		Our approach here is to omit the letter's associated prime from
		the list of primes to check while descending the expanded letter set's
		factor tree. So once the blank has been added to the set via multiplication,
		we will not remove it by division.

		This has the effect of saying, to the expanded letter set fuction:
			"DO NOT DELETE THIS NEW LETTER! YOU MUST USE IT!"
		"""

		# First, find factor tree nodes with our original letter set as the root
		factor_tree_nodes = self.factor_tree_descendants(key, self.primes)

		# Compute all possible letter sets from the given number of blanks
		blank_sets_to_add = self.combos_from_n_blanks(num_blanks)
		
		for blank_values in blank_sets_to_add:
			#print(blank_values) 				# uncomment this for a fun time
			product = 1
			primes_subset = self.primes

			for letter in blank_values:
				
				prime_factor = self.lookup[letter]
				primes_subset = [p for p in primes_subset if not p==prime_factor]
				product *= prime_factor
			
			factor_tree_nodes.extend(self.factor_tree_descendants(key*product, primes_subset))
		return factor_tree_nodes


def ui_loop():
	with open('scrabble_dictionary.txt') as f:
		legal_words = [line.strip().lower() for line in f.readlines()]
	wf = WordFinder(legal_words)
	while True:
		user_input = input('Enter letters:\n')
		letters = ''.join([c for c in user_input if not c=='?'])
		num_blanks = len([c for c in user_input if c=='?'])
		print('\n'.join(wf.words_formable_from_letters(letters, num_blanks)))


if __name__ == '__main__':
	
	ui_loop()


