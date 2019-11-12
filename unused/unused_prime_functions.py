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