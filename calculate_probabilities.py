from collections import defaultdict
import re
# import tokens_parser
import ngram_probabilities
import string


def _read_data(input_file):
    with open(input_file, "r") as file:
        return file.read()


def _get_tokens(data, regex):
    if regex:
        return re.findall(regex, data)

    tokens = re.findall(f"([-\w]+|[{string.punctuation}])", data)
    print(tokens)
    return tokens

def _get_frequences(tokens, depth):
    frequences = [defaultdict(lambda: defaultdict(int)) for length in range(depth + 1)]
    for token_index, token in enumerate(tokens):
        for length in range(depth + 1):
            if length <= token_index:
                current_sequence = tuple(tokens[token_index - length: token_index])
                frequences[length][current_sequence][token] += 1

    return frequences


def calculate_probabilities_for_text(input_file, probabilities_file, depth, regex):
    data = _read_data(input_file)
    tokens = _get_tokens(data, regex)
    print(f"input_file consists of {len(tokens)} words")
    frequences = _get_frequences(tokens, depth)
    probabilities = ngram_probabilities.NgramProbabilities(frequences=frequences, depth=depth)
    probabilities.save_probabilities(probabilities_file)
