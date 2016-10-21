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
- The longest word in the solution is 11 characters long.
- The second longest word contains 8 characters and is next to the 11 character word
- The solution does not refer to anagrams or puzzles or winning t-shirts.
- However, what T-Rex is saying is directly related to the content of the comic the puzzle appears in.
- The letters given are case-sensitive!
- The first word of the solution is "I".

Strategy
--------

- Choose compatible 8 and 11 letter words, then use recursion with backtracking to generate all possible word sets for the rest of the sentence.
- Use a trie to keep track of which characters can come next in a word.
- In making the trie, filter out words that

  - Don't fit the letter counts
  - Have 9 or 10 letter
  - Aren't dictionary words
  - Aren't in the Qwantz Corpus
  
- At any step, only consider letters that come next in the trie and are available in a running letter count.
- Only generate words in alphabetical order, to avoid generating the same word sets in different orders.

This will generate all possible sets of words that fit the requirements, which can then be permuted.

Evaluating results
------------------

How can the results be evaluated? Is there some way to rule out entire sets of words based on statistics like word length distribution? When permuting word sets, is it possible to build word by word, throwing out anything that isn't "reasonably grammatical"? Can the permutations be ranked by how "grammatical" they are, or by how well they fit T-Rex's linguistic statistics?
