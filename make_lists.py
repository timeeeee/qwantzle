from time import clock
from string import lowercase

CORPUS_FILE = "qwantzcorpus"
QWANTZLE_COUNTS = "12t10o8e7a6l6n6u5i5s5d5h5y3I3r3fbbwwkcmvg"

def is_alphabetic(word):
    for char in set(word):
        if char not in (lowercase + "I"):
            return False
    return True


def matches_counts(word, counts):
    local_counts = counts.copy()
    for char in word:
        if char not in local_counts or local_counts[char] <= 1:
            return False
        else:
            local_counts[char] -= 1
    # If we didn't run out of any characters yet, we're good
    return True


def get_corp(filename):
    with open(filename) as corpus:
        words = ["".join(line.split()[1:]) for line in corpus]
    return filter(is_alphabetic, words)


def main():
    corp_words = get_corp(CORPUS_FILE)

    words = []
    eight_letter = []
    eleven_letter = []
    for word in corp_words:
        length = len(word)
        if length < 8:
            words.append(word)
        elif length == 8:
            words.append(word)
            eight_letter.append(word)
        elif length == 11:
            words.append(word)
            eleven_letter.append(word)

    print "8 letter words:  {}".format(len(eight_letter))
    print "11 letter words: {}".format(len(eleven_letter))
    print "total:           {}".format(len(words))


if __name__ == "__main__":
    main()
