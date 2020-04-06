import string
import collections
import pickle


def _remove_trash(word):
    return "".join(filter(lambda x: x.isalpha() or x in string.punctuation, word))


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

    return prefix + [word[first_letter: last_letter + 1].lower()] + suffix[::-1]


def _get_tockens(input_file):
    with open(input_file, "r") as file:
        data = list(file.read().split())

    tockens = []
    for word in data:
        tockens += _split_punctuation(_remove_trash(word))
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


calculate("input_file.txt", "probabilities_file.txt", 3)
