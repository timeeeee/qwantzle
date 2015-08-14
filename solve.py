from utils import *

SOLUTIONS_OUT = "solutions.txt"
ELEVEN_CHAR_WORDS = load_wordlist("eleven_char_words.txt")
EIGHT_CHAR_WORDS = load_wordlist("eight_char_words.txt")
SHORT_WORDS = load_wordlist("short_words.txt")

def solve(counts, starting_word_index=0):
    """Return a generator that yields all possible solution word sets

    It will only check after a certain point in the dictionary, so that we only
    get each possible set of words once.
    """
    # pick a first word
    # NOTE this will make a copy for each recursion!!!
    for index in range(starting_word_index, len(SHORT_WORDS)):
        word = SHORT_WORDS[index]

        if matches_counts(word, counts):
            if starting_word_index == 0:
                print "solutions starting with word {}".format(word)
            new_counts = subtract_word(counts, word)
            
            # check to see if this is a solution!
            if all(count == 0 for count in new_counts.values()):
                yield [word]
            else:
                # recursively solve for the rest
                for solution in solve(new_counts, index):
                    yield [word] + solution


def solve_qwantzle():
    """Give all possible solution word sets to the WHOLE qwantzle"""
    global_counts = make_count_dict(QWANTZLE_COUNTS)
    base_solution = ["I", "I", "I"]
    global_counts["I"] -= 3

    # choose eleven letter word
    for eleven_char_word in ELEVEN_CHAR_WORDS:
        # Because the words have been filtered we know it fits
        counts_after_eleven = subtract_word(global_counts, eleven_char_word)
        print "chose 11 letter word {}".format(eleven_char_word)

        # choose eight letter word
        for eight_char_word in EIGHT_CHAR_WORDS:
            print "    chose 8 letter word {}".format(eight_char_word)
            if matches_counts(eight_char_word, counts_after_eleven):
                counts = subtract_word(counts_after_eleven, eight_char_word)
                for partial_solution in solve(counts):
                    sentence = " ".join(base_solution + [eleven_char_word] +
                                        [eight_char_word] + partial_solution)
                    print sentence
                    yield sentence
            else:
                 print "NNNOOOOOOOPPPPEEEEE"   


def main():
    with open(SOLUTIONS_OUT, 'w') as outfile:
        for solution in solve_qwantzle():
            outfile.write(solution)


if __name__ == "__main__":
    main()
