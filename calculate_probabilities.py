import collections
import pickle
import re
import tokens_parser


def _read_tokens(input_file):
    with open(input_file, "r") as file:
        data = list(file.read().split())
    return data


def _get_tokens(data, regex):
    if regex:
        tokens = []
        for word in data:
            tokens += re.findall(regex, word)
        return tokens

    return tokens_parser.get_tokens(data)


def _get_probabilities(tokens, depth):
    probabilities = dict()
    sequences = [collections.deque() for i in range(depth)]
    for i in range(len(tokens)):
        for length in range(1, depth + 1):
            sequences[length - 1].append(tokens[i])
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


def calculate(input_file, probabilities_file, depth, regex):
    data = _read_tokens(input_file)
    tokens = _get_tokens(data, regex)
    probabilities = _get_probabilities(tokens, depth)
    _save_probabilities(probabilities, probabilities_file)
