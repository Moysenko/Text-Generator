import pickle
import collections
import random
import string
import sys


def _get_probability(probability_file):
    with open(probability_file, "rb") as file:
        probability = pickle.load(file)
    return probability


def _get_punctuation_pair(char):
    if char in '()':
        return '()'[char == '(']
    else:
        return char


def _get_random_token(probability):
    random_number = random.random()
    for token, chance in probability.items():
        if random_number < chance:
            return token
        else:
            random_number -= chance


def _is_valid_token(text, token, stack):
    if (not text or text[-1] in string.punctuation) and token in string.punctuation:
        return False
    if token == ')' and (not stack or stack[-1] != '('):
        return False
    return True


def _get_random_valid_token(text, probability, stack):
    attempts = 100
    while True:
        token = _get_random_token(probability)
        if _is_valid_token(text, token, stack):
            return token
        attempts -= 1
        if not attempts:
            print("ERROR!!!", text, probability)
            sys.exit(228)


def _modifyed_token(text, token):
    if (not token.isalpha() and token != '(') or (text and text[-1] == '('):
        return token
    if len(text) == 0:
        return token.capitalize()
    if text[-1] in '.?!':
        return ' ' + token.capitalize()
    return ' ' + token


def _generate_text(probability, depth, tokens_amount):
    last_tokens = collections.deque()
    text = ''
    stack = []  # stack of opened brackets and quotes
    for step in range(tokens_amount):
        while (len(last_tokens) > depth) or (not tuple(last_tokens) in probability) or\
                not list(filter(lambda token: _is_valid_token(text, token, stack),
                                probability[tuple(last_tokens)].keys())):
            last_tokens.popleft()
        token = _get_random_valid_token(text, probability[tuple(last_tokens)], stack)

        if token in '?!.' and stack:
            token = _get_punctuation_pair(stack[-1])
            stack.pop()

        text += _modifyed_token(text, token)
        last_tokens.append(token)

        if token in '()"\'':
            if stack and stack[-1] == _get_punctuation_pair(token):
                stack.pop()
            else:
                stack.append(token)
    return text


def _write_text(output_file, text):
    if output_file == 'to console':
        print(text)
    else:
        with open(output_file, "w") as file:
            file.write(text)


def generate(probability_file, depth, tokens_amount, output_file):
    probability = _get_probability(probability_file)
    text = _generate_text(probability, depth, tokens_amount)
    _write_text(output_file, text)
