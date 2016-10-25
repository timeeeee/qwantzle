Qwantzle solver
===============

Solve [The Qwantzle](http://qwantz.com/index.php?comic=1663) anagram from Dinosaur Comics, with this letter count:
12t10o8e7a6l6n6u5i5s5d5h5y3I3r3fbbwwkcmvg

Hints
-----

- All words in the solution are dictionary words.
- What's more, all words in the solution are in the Jadrian's awesome Qwantz Corpus!
- The solution is natural-sounding, reasonably-grammatical dialogue that T-Rex would say, using phrasing that T-Rex would use.
- The punctuation :,!! is in the solution, in that order!
- The longest word in the solution is "fundamental".
- The second longest word contains 8 characters and is next to the word "fundamental".
- The solution does not refer to anagrams or puzzles or winning t-shirts.
- However, what T-Rex is saying is directly related to the content of the comic the puzzle appears in.
- The letters given are case-sensitive!
- The first word of the solution is "I".

Strategy
--------

1. Create two wordlists that match the qwantzle letter counts minus 3 I's and "fundamental", one with 8-letter words and one with shorter words, filtering out words from a blacklist.
2. For each 8 letter word:

  1. Further filter the short word list to remove anything that doesn't match the letter counts minus the chosen 8-letter word.
  2. Build a trie from the remaining words.
  3. Recursively guess letters from the trie, backtracking when running out of available letters.

Only generate words in alphabetical order; this will generate all possible sets of words that fit the requirements, which can then be permuted.

Evaluating results
------------------

How can the results be evaluated? Is there some way to rule out entire sets of words based on statistics like word length distribution? When permuting word sets, is it possible to build word by word, throwing out anything that isn't "reasonably grammatical"? Can the permutations be ranked by how "grammatical" they are, or by how well they fit T-Rex's linguistic statistics?
