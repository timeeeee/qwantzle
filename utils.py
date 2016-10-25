from string import digits
QWANTZLE_COUNTS = "12t10o8e7a6l6n6u5i5s5d5h5y3I3r3fbbwwkcmvg"

def matches_counts(word, counts):
    """Check if there are enough characters to make up a word"""
    local_counts = counts.copy()
    for char in word:
        if char not in local_counts or local_counts[char] == 0:
            return False
        else:
            local_counts[char] -= 1
    # If we didn't run out of any characters yet, we're good
    return True


def make_count_dict(count_string):
    """Make dict of character counts from an anagram string"""
    count_list = list(count_string)
    count_dict = dict()
    number_string = ""
    while count_list:
        char = count_list.pop(0)
        if char in digits:
            number_string += char
        else:
            if number_string:
                number = int(number_string)
            else:
                number = 1
            count_dict[char] = number
            number_string = ""
    return count_dict


def subtract_word(counts, word):
    """Create a copy of character count dictionary, minus a word"""
    new_counts = counts.copy()
    for char in word:
        new_counts[char] -= 1

    if any(count < 0 for count in new_counts.values()):
        raise ValueError('Cannot subtract word "{}" from counts {}'.format(
            word, counts))

    return new_counts


def load_wordlist(filename):
    """Load word list from a file into a list of strings"""
    with open(filename) as f:
        return [line.strip() for line in f]


def load_corpus(filename):
    """Load word list from file with format <count> <word>"""
    with open(filename) as f:
        return [line.split()[1] for line in f]
