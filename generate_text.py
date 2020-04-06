import pickle
import collections


def _get_probability(probability_file):
    with open(probability_file, "rb") as file:
        probability = pickle.load(file)
    return probability


def _generate_text(probability, depth, tokens_amount):
    last_tokens = collections.deque()
    text = ''
    for step in range(tokens_amount):
        while not tuple(last_tokens) in probability:
            last_tokens.popleft()
        token = _get_random(probability[tuple(last_tokens)])



def generate(probability_file, depth, tokens_amount, output_file):
    probability = _get_probability(probability_file)
    text = _generate_text(probability, depth, tokens_amount)


generate("probabilities_file.txt", 3, 5, "output_file.txt")
