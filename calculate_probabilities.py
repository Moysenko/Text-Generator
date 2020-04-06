import string
import collections
import pickle


def _remove_trash(word):
    filtered_word =  ''.join([char if (char.isalpha() or char in string.punctuation) else ' ' for char in word])
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


def _get_tockens(input_file):
    with open(input_file, "r") as file:
        data = list(file.read().split())

    filtered_data = []
    for word in data:
        filtered_data += _remove_trash(word)

    tockens = []
    for word in filtered_data:
        tockens += _split_punctuation(word)
    return tockens


def _get_probabilities(tockens, depth):
    probabilities = dict()
    sequences = [collections.deque() for i in range(depth)]
    for i in range(len(tockens)):
        for length in range(1, depth + 1):
            sequences[length - 1].append(tockens[i])
            if length < i + 1:
                sequences[length - 1].popleft()
            if length <= i + 1:
                current_sequence = tuple(sequences[length - 1])[:length - 1]
                current_ending = sequences[length - 1][-1]
                if current_sequence in probabilities:
                    occurrences_amount = probabilities[current_sequence].get(current_ending, 0)
                    probabilities[current_sequence][current_ending] = occurrences_amount + 1
                else:
                    probabilities[current_sequence] = {current_ending: 1}

    for sequence, endings in probabilities.items():
        endings_amount = sum(endings.values())
        for ending in endings.keys():
            probabilities[sequence][ending] /= endings_amount

    return probabilities


def _save_probabilities(probabilities, probabilities_file):
    with open(probabilities_file, "wb") as file:
        pickle.dump(probabilities, file)


def calculate(input_file, probabilities_file, depth):
    tockens = _get_tockens(input_file)
    probabilities = _get_probabilities(tockens, depth)
    _save_probabilities(probabilities, probabilities_file)
