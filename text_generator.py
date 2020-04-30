import collections
import random
import string
import punctuation
import tokens_parser


class Generator:
    MAX_GENERATE_ATTEMPTS = 100

    def __init__(self, probability, depth, uniform_proba):
        self.probability = probability
        self.depth = depth
        self.uniform_proba = uniform_proba
        self.reset()

    def _is_valid_token(self, token):
        if token in punctuation.CLOSE_BRACKETS and token not in punctuation.OPEN_BRACKETS and\
                (not self.opening_brackets_stack or
                 punctuation.PUNCTUATION_PAIR[self.opening_brackets_stack[-1]] != token):
            return False
        if self.text and (self.text[-1] in punctuation.CLOSE_BRACKETS or
                          (self.text[-1] + token) in punctuation.VALID_PUNCTUATION_PAIRS):
            return True
        if (not self.text or self.text[-1] in string.punctuation) and token in string.punctuation:
            return False
        return True

    def _get_modifyed_token(self, token):
        if token == '-':
            return ' ' + token
        if token in punctuation.OPEN_BRACKETS and token in punctuation.CLOSE_BRACKETS:
            if self.opening_brackets_stack and self.opening_brackets_stack[-1] == token:
                return token
            else:
                return ' ' + token
        if token.isalpha() and self.text and \
                self.text[-1] in punctuation.OPEN_BRACKETS and self.text[-1] in punctuation.CLOSE_BRACKETS:
            if self.opening_brackets_stack and self.opening_brackets_stack[-1] == self.text[-1]:
                return token
            else:
                return ' ' + token
        if (not token.isalpha() and token not in punctuation.OPEN_BRACKETS) or\
                (self.text and self.text[-1] in punctuation.OPEN_BRACKETS):
            return token
        if not self.text:
            return token.capitalize()
        if self.text[-1] in punctuation.SENTENCE_ENDING_PUNCTUATION:
            return ' ' + token.capitalize()
        return ' ' + token

    def _get_valid_tokens(self, ngram):
        return [token for token in self.probability.get_ngram_endings(ngram) if self._is_valid_token(token[0])]

    def _get_random_valid_token(self, key):
        valid_tokens = self._get_valid_tokens(key)
        assert valid_tokens, f"Error: no valid tokens found.\nkey: {key}, last tokens: {self.last_tokens_id}"
        max_probability = sum(token[1] for token in valid_tokens)
        choice = random.uniform(0, max_probability)
        for token, probability in valid_tokens:
            if choice < probability:
                return token
            choice -= probability

    def _make_valid_last_tokens_id(self):
        while (len(self.last_tokens_id) > self.depth) or\
                (tuple(self.last_tokens_id) not in self.probability.probabilities) or\
                not self._get_valid_tokens(tuple(self.last_tokens_id)):
            self.last_tokens_id.popleft()

    def _update_punctuation_stack(self, token):
        if token in punctuation.PAIRED_PUNCTUATION:
            if self.opening_brackets_stack and self.opening_brackets_stack[-1] == punctuation.PUNCTUATION_PAIR[token]:
                self.opening_brackets_stack.pop()
            else:
                self.opening_brackets_stack.append(token)

    def _get_generating_step(self, sentence_ending):
        is_step_skipped = False
        if sentence_ending:
            if not self.opening_brackets_stack:
                token = sentence_ending
                sentence_ending = None
            else:
                token = punctuation.PUNCTUATION_PAIR[self.opening_brackets_stack[-1]]
        else:
            self._make_valid_last_tokens_id()
            key = () if random.random() < self.uniform_proba else tuple(self.last_tokens_id)
            token = self._get_random_valid_token(key)

            if token in punctuation.SENTENCE_ENDING_PUNCTUATION and self.opening_brackets_stack:
                sentence_ending = token
                is_step_skipped = True

        return token, is_step_skipped, sentence_ending

    def add_text(self, tokens_amount):
        sentence_ending = None
        tokens_generated = 0
        while tokens_generated < tokens_amount:
            token, is_step_skipped, sentence_ending = self._get_generating_step(sentence_ending)

            if is_step_skipped:
                continue

            modifyed_token = self._get_modifyed_token(token)
            self.text += modifyed_token
            self.last_tokens_id.append(self.probability.token_to_id[token])

            self._update_punctuation_stack(token)
            tokens_generated += 1

    def reset(self):
        self.last_tokens_id = collections.deque()
        self.text = ''
        self.opening_brackets_stack = []

    def set_last_tokens_id(self, data):
        tokens = tokens_parser.get_tokens(data)
        self.probability._add_tokens(tokens)
        tokens_id = [self.probability.token_to_id[token] for token in tokens]
        self.last_tokens_id = collections.deque(tokens_id)

    def get_probability(self, amount=10):
        self._make_valid_last_tokens_id()
        possible_tokens = self.probability.get_ngram_endings(tuple(self.last_tokens_id))
        possible_tokens.sort(key=lambda item: -item[1])
        return possible_tokens[:amount]

    def set_depth(self, depth):
        self.depth = depth

    def get_text(self):
        return self.text
