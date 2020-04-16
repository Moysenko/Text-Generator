import collections
import pickle
import re
import tokens_parser


def _read_tokens(input_file):
    with open(input_file, "r") as file:
        return list(file.read().split())


def _get_tokens(data, regex):
    if regex:
        tokens = []
        for word in data:
            tokens += re.findall(regex, word)
        return tokens

    return tokens_parser.get_tokens(data)

def _default_dict_with_int_constructor():
    return collections.defaultdict(int)

def _get_frequences(tokens, depth):
    frequences = [collections.defaultdict(_default_dict_with_int_constructor)
                  for length in range(depth + 1)]
    for token_index, token in enumerate(tokens):
        for length in range(0, depth + 1):
            if length <= token_index:
                current_sequence = tuple(tokens[token_index - length: token_index])
                frequences[length][current_sequence][token] += 1

    return frequences


def _get_D(frequences):
    N12 = [0, 0]
    for endings in frequences.values():
        count = sum(endings.values())
        if 1 <= count <= 2:
            N12[count - 1] += 1
    D = N12[0] / (N12[0] + 2 * N12[1]) if N12[0] + N12[1] > 0 else 0
    return D


def _calc_reversed_pairs(frequences, word_to_id):
    pairs = collections.defaultdict(int)
    for value in frequences.values():
        for key in value.keys():
            pairs[word_to_id[key]] += 1
    return pairs


def _calc_words_id(words):
    word_to_id = collections.defaultdict(int)
    id_to_word = list(words)
    for word_id, word in enumerate(words):
        word_to_id[word] = word_id
    return word_to_id, id_to_word


def _get_deque_id(deque, word_to_id):
    return tuple(word_to_id[word] for word in deque)


def _calc_ngrams(probabilities, frequences, depth, word_to_id, id_to_word):
    pairs = _calc_reversed_pairs(frequences[1], word_to_id)
    total_pairs = sum(pairs.values())

    counter = 0
    for n in range(1, depth + 1):
        D = _get_D(frequences[n])
        for ngram, endings in frequences[n].items():
            total = sum(endings.values())
            alpha = D * len(endings) / total
            ngram_id = _get_deque_id(ngram, word_to_id)
            for token in probabilities[()].keys():
                first_part = max(endings[id_to_word[token]] - D, 0) / total
                if n == 1:  # bigram
                    Pkn = pairs[token] / total_pairs
                else:  # n-gram
                    Pkn = probabilities[ngram_id[1:]][token]
                probabilities[ngram_id][token] = first_part + alpha * Pkn
                counter += 1


def _get_probabilities(frequences, depth):
    probabilities = collections.defaultdict(_default_dict_with_int_constructor)

    word_to_id, id_to_word = _calc_words_id(frequences[0][()].keys())

    # calc for 0-gram
    probabilities[()] = collections.defaultdict(int, [(word_to_id[token], frequence)
                                                      for token, frequence in frequences[0][()].items()])
    total = sum(probabilities[()].values())
    for token in probabilities[()]:
        probabilities[()][token] /= total

    print(len(probabilities[()]))

    # using the equation for n-grams and for bigram
    _calc_ngrams(probabilities, frequences, depth, word_to_id, id_to_word)

    return probabilities, id_to_word


def _save_probabilities(probabilities, id_to_word, probabilities_file):
    with open(probabilities_file, "wb") as file:
        pickle.dump(probabilities, file)
        pickle.dump(id_to_word, file)


def calculate_probabilities_for_text(input_file, probabilities_file, depth, regex):
    data = _read_tokens(input_file)
    tokens = _get_tokens(data, regex)
    frequences = _get_frequences(tokens, depth)
    probabilities, id_to_word = _get_probabilities(frequences, depth)
    _save_probabilities(probabilities, id_to_word, probabilities_file)
