
def letters_for_anagram_key(self, key):
	#factors = [f for f in self.factor_tree_descendants(key) if f in self.primes]
	factors = self.factorize(key)		# TODO: properly factorize instead of finding unique factors
	letters = [self.reverse_lookup[f] for f in factors]
	return ''.join(letters)

def factorize(self, n):
	"""
	Return a list of prime factors of n
	"""
	factors = []
	i = 2
	limit = n//2
	while i <= limit:
		while n%i == 0:
			factors.append(i)
			n = n / i
		i = i + 1
	if len(factors) == 0:
		factors = [n]
	return factors