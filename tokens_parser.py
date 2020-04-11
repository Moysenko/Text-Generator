import string


def _remove_trash(word):
    filtered_word = ''.join([char if (char.isalpha() or char in string.punctuation) else ' ' for char in word])
    return list(filtered_word.split())


def _split_punctuation(word):
    first_letter = 0
    prefix = []
    while first_letter < len(word) and not word[first_letter].isalpha():
        prefix.append(word[first_letter])
        first_letter += 1

    last_letter = len(word) - 1
    suffix = []
    while last_letter > first_letter and not word[last_letter].isalpha():
        suffix.append(word[last_letter])
        last_letter -= 1

    middle = []
    if first_letter <= last_letter:
        middle = [word[first_letter: last_letter + 1].lower()]

    return prefix + middle + suffix[::-1]


def get_tokens(raw_data):
    filtered_data = []
    for word in raw_data:
        filtered_data += _remove_trash(word)

    tokens = []
    for word in filtered_data:
        tokens += _split_punctuation(word)
    return tokens
