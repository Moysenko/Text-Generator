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
    for token_index, token in enumerate(tokens):
        for length in range(0, depth + 1):
            sequences[length].append(token)
            if length < token_index:
                sequences[length].popleft()
            if length <= token_index:
                current_sequence = tuple(sequences[length])[:length]
                if current_sequence in frequences[length]:
                    occurrences_amount = frequences[length][current_sequence].get(token, 0)
                    frequences[length][current_sequence][token] = occurrences_amount + 1
                else:
                    frequences[length][current_sequence] = {token: 1}

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


def _calc_reversed_pairs(frequences, word_to_id):
    pairs = {}
    for value in frequences.values():
        for key in value.keys():
            _add_to_dict(pairs, word_to_id[key])
    return pairs


def _calc_words_id(words):
    word_to_id, id_to_word = {}, {}
    for id, word in enumerate(words):
        id_to_word[id] = word
        word_to_id[word] = id
    return word_to_id, id_to_word


def _get_deque_id(deque, word_to_id):
    return tuple(word_to_id[word] for word in deque)


def _get_probabilities(frequences, depth):
    probabilities = dict()

    word_to_id, id_to_word = _calc_words_id(frequences[0][()].keys())

    for n in range(depth + 1):
        for key in frequences[n].keys():
            probabilities[_get_deque_id(key, word_to_id)] = {}

    # calc for 0-gram
    probabilities[()] = {word_to_id[word]: frequence for word, frequence in frequences[0][()].items()}
    total = sum(probabilities[()].values())
    for token in probabilities[()]:
        probabilities[()][token] /= total

    print(len(probabilities[()]))

    pairs = _calc_reversed_pairs(frequences[1], word_to_id)
    total_pairs = sum(pairs.values())

    # using the equation for n-grams and for bigram
    counter = 0
    for n in range(1, depth + 1):
        D = _get_D(frequences[n])
        for ngram, endings in frequences[n].items():
            total = sum(endings.values())
            alpha = D * len(endings) / total
            ngram_id = _get_deque_id(ngram, word_to_id)
            for token in probabilities[()].keys():
                first_part = max(endings.get(id_to_word[token], 0) - D, 0) / total
                if n == 1:  # bigram
                    Pkn = pairs.get(token, 0) / total_pairs
                else:  # n-gram
                    Pkn = probabilities[ngram_id[1:]][token]
                probabilities[ngram_id][token] = first_part + alpha * Pkn
                counter += 1

    return probabilities, id_to_word


def _save_probabilities(probabilities, id_to_word, probabilities_file):
    with open(probabilities_file, "wb") as file:
        pickle.dump(probabilities, file)
        pickle.dump(id_to_word, file)


def calculate(input_file, probabilities_file, depth, regex):
    data = _read_tokens(input_file)
    tokens = _get_tokens(data, regex)
    frequences = _get_frequences(tokens, depth)
    probabilities, id_to_word = _get_probabilities(frequences, depth)
    _save_probabilities(probabilities, id_to_word, probabilities_file)
