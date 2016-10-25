"""
Generate word lists to use for the Qwantzle.

In the clues, Ryan North indicates that all words in the solution are in
Jadrian's qwantz corpus, and that they're dictionary words. This script will
output two lists, one with words that are 8 letters long, one with words
shorter than 8 letters.

Since the first word of the solution is I, and the 11 letter word is
"fundamental", we can filter out any words that aren't possible within the
problem letter counts, minus "I", minus "fundamental".

Since the solution contains no apostrophe's, any contractions etc. will be
filtered out.

In terms of algorithmic complexity, it's probably better to re-filter the short
words list for each 8-letter word.
"""

from string import lowercase, digits

from utils import *

# In: All words used by T-Rex
CORPUS_FILE = "qwantzcorpus"
# In: Blacklist (words to skip)
BLACKLIST_FILE = "blacklist.txt"
# Out: Words that are shorter than 8 characters
SHORT_OUT = "short_words.txt"
# Out: Eight character words
EIGHT_OUT = "eight_char_words.txt"


def get_corpus(filename):
    with open(filename) as corpus:
        words = ["".join(line.split()[1:]) for line in corpus]
    return filter(is_alphabetic, words)


if __name__ == "__main__":
    corp_words = [word for word in load_corpus(CORPUS_FILE) if word.isalpha()]

    # Get qwantz counts, minus 3*I and fundamental
    letter_counts = make_count_dict(QWANTZLE_COUNTS)
    letter_counts = subtract_word(letter_counts, "I")
    letter_counts = subtract_word(letter_counts, "I")
    letter_counts = subtract_word(letter_counts, "I")
    letter_counts = subtract_word(letter_counts, "fundamental")

    blacklist = set(load_wordlist(BLACKLIST_FILE))
    
    short = []
    eight_letter = []

    for word in corp_words:
        if matches_counts(word, letter_counts) and word not in blacklist:
            length = len(word)
            if length < 8:
                short.append(word)
            elif length == 8:
                eight_letter.append(word)

    short.sort()
    with open(SHORT_OUT, "w") as short_out:
        for word in short:
            short_out.write(word + "\n")

    eight_letter.sort()
    with open(EIGHT_OUT, "w") as eight_out:
        for word in eight_letter:
            eight_out.write(word + "\n")

    print "<8 letter words: {}".format(len(short))
    print "8 letter words:  {}".format(len(eight_letter))
