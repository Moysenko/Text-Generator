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


def _get_frequences(tokens, depth):
    frequences = [dict() for length in range(depth + 1)]
    sequences = [collections.deque() for i in range(depth + 1)]
    for i in range(len(tokens)):
        for length in range(0, depth + 1):
            sequences[length].append(tokens[i])
            if length < i:
                sequences[length].popleft()
            if length <= i:
                current_sequence = tuple(sequences[length])[:length]
                current_ending = sequences[length][-1]
                if current_sequence in frequences[length]:
                    occurrences_amount = frequences[length][current_sequence].get(current_ending, 0)
                    frequences[length][current_sequence][current_ending] = occurrences_amount + 1
                else:
                    frequences[length][current_sequence] = {current_ending: 1}

    return frequences


def _get_D(frequences):
    N12 = [0, 0]
    for endings in frequences.values():
        count = sum(endings.values())
        if 1 <= count <= 2:
            N12[count - 1] += 1
    D = N12[0] / (N12[0] + 2 * N12[1]) if N12[0] + N12[1] > 0 else 0
    return D


def _add_to_dict(dictionary, key):
    if key in dictionary:
        dictionary[key] += 1
    else:
        dictionary[key] = 1


def _calc_reversed_pairs(frequences):
    pairs = {}
    for value in frequences.values():
        for key in value.keys():
            _add_to_dict(pairs, key)
    return pairs


def _get_probabilities(frequences, depth):
    probabilities = dict()
    for n in range(depth + 1):
        for key in frequences[n].keys():
            probabilities[key] = {}

    # calc for 0-gram
    probabilities[()] = frequences[0][()]
    total = sum(probabilities[()].values())
    for token in probabilities[()]:
        probabilities[()][token] /= total

    pairs = _calc_reversed_pairs(frequences[1])
    total_pairs = sum(pairs.values())

    # using the equation for n-grams and for bigram
    for n in range(1, depth + 1):
        D = _get_D(frequences[n])
        for ngram, endings in frequences[n].items():
            total = sum(endings.values())
            alpha = D * len(endings) / total
            for token in probabilities[()].keys():
                first_part = (endings[token] - D) / total if token in endings else 0
                if n == 1:  # bigram
                    Pkn = pairs.get(token, 0) / total_pairs
                else:  # n-gram
                    Pkn = probabilities[tuple(ngram)[1:]][token]
                probabilities[tuple(ngram)][token] = first_part + alpha * Pkn

    return probabilities


def _save_probabilities(probabilities, probabilities_file):
    with open(probabilities_file, "wb") as file:
        pickle.dump(probabilities, file)


def calculate(input_file, probabilities_file, depth, regex):
    data = _read_tokens(input_file)
    tokens = _get_tokens(data, regex)
    frequences = _get_frequences(tokens, depth)
    probabilities = _get_probabilities(frequences, depth)
    _save_probabilities(probabilities, probabilities_file)
