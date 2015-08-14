QWANTZLE_COUNTS = "12t10o8e7a6l6n6u5i5s5d5h5y3I3r3fbbwwkcmvg"

def matches_counts(word, counts):
    local_counts = counts.copy()
    for char in word:
        if char not in local_counts or local_counts[char] == 0:
            return False
        else:
            local_counts[char] -= 1
    # If we didn't run out of any characters yet, we're good
    return True


def make_count_dict(count_string):
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
    new_counts = counts.copy()
    for char in word:
        new_counts[char] -= 1

    if any(count < 0 for count in new_counts.values()):
        raise ValueError('Cannot subtract word "{}" from counts {}'.format(
            word, counts))
