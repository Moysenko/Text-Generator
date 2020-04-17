import collections
import pickle
import re
import tokens_parser
import NgramProbabilities


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


def _save_probabilities(probabilities, probabilities_file):
    with open(probabilities_file, "wb") as file:
        pickle.dump(probabilities.probabilities, file)
        pickle.dump(probabilities.id_to_word, file)


def calculate_probabilities_for_text(input_file, probabilities_file, depth, regex):
    data = _read_tokens(input_file)
    tokens = _get_tokens(data, regex)
    frequences = _get_frequences(tokens, depth)
    probabilities = NgramProbabilities.NgramProbabilities(frequences, depth)
    _save_probabilities(probabilities, probabilities_file)
