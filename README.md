# anagrams

A library for playing and analyzing the game of [Snatch](https://en.wikipedia.org/wiki/Anagrams).

To run the main script:
`python snatch.py`

————

## `models/game.py`

The `Game` class represents:
- Letters on the shared board
- Players and the words they own

## `models/word_finder.py`

The `WordFinder` class represents:
- A list of legal words and their frequencies
- The letters of the alphabet and their associated primes
- An anagram dictionary mapping letter sets to word sets via the letters' prime hash

### Some WordFinder methods:

`anagram_key_for_letters(self, letters)`
Find a letter set's hash by multiplying together the primes associated with each letter in the set. Words containing the same set of letters yield the same product.

`build_anagram_dictionary(self, words)`
Build a dictionary where each key is the unique hash for a letter set and each value is the set of words using all its letters.

`words_formable_from_letters(self, letters, num_blanks=0)`
Find all words formable with any subset of the given letters and up to [num_blanks] blank wildcards.

`get_factor_tree_nodes(self, key, num_blanks=0)`
Given a key representing a letter set, find keys for all unique letter sets formable by removing any number of letters and  adding up to [num_blanks] letters.

*Note on handling blanks*

When adding a letter to the letter set, we want to find all the letter sets it enables, but we need to AVOID duplicating any of the letter sets that were already possible WITHOUT the blank.

Our approach here is to omit the letter's associated prime from the list of primes to check while descending the expanded letter set's factor tree. So once the blank has been added to the set via multiplication, we will not remove it by division.

This has the effect of saying, to the expanded letter set fuction:
	"DO NOT DELETE THIS NEW LETTER! YOU MUST USE IT!"

`factor_tree_descendants(self, n, primes=None, start_index=0)`
Returns a list of keys at all nodes in the factor tree with n as the root by trying to divide by all primes in the list after a given start_index.

We move the start index at each level to ensure that we only report each node once.

Example: If the given key is 150, we could reach the node at 10 by two paths: by dividing by 3 then 5, OR 5 then 3. 

We avoid this by only checking primes that are equal to or greater than the highest prime checked in the current branch. In our example, once we have divided 150 by 5 to get 30, we move that branch's start index to 5, so we won't try dividing by 3.

`find_binary_compounds(self, word, min_size)`
Find all ways (if there are any) to split word into valid subsets of letters of at least min_size.

`difference_between_words(self, small, big)`
Given a big word that contains all the letters of a smaller word, find the letters we need to add to the smaller word to make the bigger word.
- e.g. difference_between_words(THETA, THREAT) --> 'R'

`snowball_paths_for_word(self, word)`
Given a key representing a word, return a list of all ways to remove one letter from the set and get a valid set, descending the tree until this is no longer possible.

