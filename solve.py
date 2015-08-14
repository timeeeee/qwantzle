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
    pass


def solve_qwantzle():
    """Give all possible solution word sets to the WHOLE qwantzle"""
    counts = make_count_dict(QWANTZLE_COUNTS)
    base_solution = ["I", "I", "I"]
    global_counts["I"] -= 3

    # choose eleven letter word
    for eleven_char_word in ELEVEN_CHAR_WORDS:
        counts_after_eleven = subtract_word(global_counts, eleven_char_word)

        # choose eight letter word
        for eight_char_word in EIGHT_CHAR_WORDS:
            if matches_counts(counts_after_eleven, eight_char_word):
                counts = subtract_word(counts_after_eleven, eight_char_word)
                for partial_solution in solve(counts):
                    yield (base_solution + eleven_letter_word +
                           eight_letter_word + partial_solution)


def main():
    with open(SOLUTIONS_OUT) as outfile:
        for solution in solve_qwantzle():
            outfile.write(solution)


if __name__ == "__main__":
    main()
