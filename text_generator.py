import collections
import random
import sys
import string
import punctuation
import tokens_parser


class generator:
    def __init__(self, probability, depth, uniform_proba):
        self.probability = probability
        self.depth = depth
        self.uniform_proba = uniform_proba
        self.reset()

    def _is_valid_token(self, token):
        if token in punctuation.close_brackets and\
                (not self.stack or punctuation.get_punctuation_pair(self.stack[-1]) != token):
            return False
        if self.text and (self.text[-1] in punctuation.close_brackets or
                          (self.text[-1] + token) in punctuation.valid_punctuation_pairs):
            return True
        if (not self.text or self.text[-1] in string.punctuation) and token in string.punctuation:
            return False
        return True

    def _modifyed_token(self, token):
        if token == '-':
            return ' ' + token
        if (not token.isalpha() and token not in punctuation.open_brackets) or\
                (self.text and self.text[-1] in punctuation.open_brackets):
            return token
        if not self.text:
            return token.capitalize()
        if self.text[-1] in punctuation.sentence_ending_punctuation:
            return ' ' + token.capitalize()
        return ' ' + token

    def _get_random_token(self, key):
        random_number = random.random()
        for token, chance in self.probability[key].items():
            if random_number < chance:
                return token
            else:
                random_number -= chance

    def _get_random_valid_token(self, key):
        attempts = 100
        while True:
            token = self._get_random_token(key)
            if self._is_valid_token(token):
                return token
            attempts -= 1
            if not attempts:
                print("ERROR!!!", self.text, self.probability[key])
                sys.exit(228)

    def _get_valid_last_tokens(self):
        while (len(self.last_tokens) > self.depth) or (tuple(self.last_tokens) not in self.probability) or\
                not list(filter(lambda token: self._is_valid_token(token),
                                self.probability[tuple(self.last_tokens)].keys())):
            self.last_tokens.popleft()

    def _update_punctuation_stack(self, token):
        if token in punctuation.paired_punctuation:
            if self.stack and self.stack[-1] == punctuation.get_punctuation_pair(token):
                self.stack.pop()
            else:
                self.stack.append(token)

    def add_text(self, tokens_amount):
        for step in range(tokens_amount):
            self._get_valid_last_tokens()
            key = () if random.random() < self.uniform_proba else tuple(self.last_tokens)
            token = self._get_random_valid_token(key)

            if token in punctuation.sentence_ending_punctuation and self.stack:
                token = punctuation.get_punctuation_pair(self.stack[-1])
                self.stack.pop()

            self.text += self._modifyed_token(token)
            self.last_tokens.append(token)

            self._update_punctuation_stack(token)

    def reset(self):
        self.last_tokens = collections.deque()
        self.text = ''
        self.stack = []

    def set_last_tokens(self, data):
        tokens = tokens_parser.get_tokens(data)
        self.last_tokens = collections.deque(tokens)

    def get_probability(self, amount=10):
        self._get_valid_last_tokens()
        possible_tokens = list(self.probability[tuple(self.last_tokens)].items())
        print(self.last_tokens)
        possible_tokens.sort(key=lambda item: item[1], reverse=True)
        return possible_tokens[:amount]

    def set_depth(self, depth):
        self.depth = depth

    def get_text(self):
        return self.text
