from string import lowercase, digits

from utils import *

CORPUS_FILE = "qwantzcorpus"
FILTERED_OUT = "filtered_words.txt"
SHORT_OUT = "short_words.txt"
EIGHT_OUT = "eight_char_words.txt"
ELEVEN_OUT = "eleven_char_words.txt"
BLACKLIST_FILE = "blacklist.txt"

def is_alphabetic(word):
    for char in set(word):
        if char not in (lowercase + "I"):
            return False
    return True


def get_corp(filename):
    with open(filename) as corpus:
        words = ["".join(line.split()[1:]) for line in corpus]
    return filter(is_alphabetic, words)


def main():
    corp_words = get_corp(CORPUS_FILE)
    letter_counts = make_count_dict(QWANTZLE_COUNTS)

    blacklist = load_wordlist(BLACKLIST_FILE)
    
    short = []
    words = []
    eight_letter = []
    eleven_letter = []
    for word in corp_words:
        if matches_counts(word, letter_counts) and word not in blacklist:
            length = len(word)
            if length < 8:
                short.append(word)
                words.append(word)
            elif length == 8:
                words.append(word)
                eight_letter.append(word)
            elif length == 11:
                words.append(word)
                eleven_letter.append(word)

    with open(FILTERED_OUT, "w") as filtered_out:
        for word in words:
            filtered_out.write(word + "\n")

    with open(SHORT_OUT, "w") as short_out:
        for word in short:
            short_out.write(word + "\n")

    with open(EIGHT_OUT, "w") as eight_out:
        for word in eight_letter:
            eight_out.write(word + "\n")

    with open(ELEVEN_OUT, "w") as eleven_out:
        for word in eleven_letter:
            eleven_out.write(word + "\n")
            
    print "<8 letter words: {}".format(len(short))
    print "8 letter words:  {}".format(len(eight_letter))
    print "11 letter words: {}".format(len(eleven_letter))
    print "total:           {}".format(len(words))

    


if __name__ == "__main__":
    main()
