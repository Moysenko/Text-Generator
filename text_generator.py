import collections
import random
import sys
import string
import punctuation
import tokens_parser


class generator:
    def __init__(self, probability, id_to_word, depth, uniform_proba):
        self.probability = probability
        self.id_to_word = id_to_word
        self.word_to_id = {word: id for id, word in self.id_to_word.items()}
        self.depth = depth
        self.uniform_proba = uniform_proba
        self.reset()

    def _is_valid_token(self, token):
        if token in punctuation.CLOSE_BRACKETS and\
                (not self.stack or punctuation.get_punctuation_pair(self.stack[-1]) != token):
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
        if (not token.isalpha() and token not in punctuation.OPEN_BRACKETS) or\
                (self.text and self.text[-1] in punctuation.OPEN_BRACKETS):
            return token
        if not self.text:
            return token.capitalize()
        if self.text[-1] in punctuation.SENTENCE_ENDING_PUNCTUATION:
            return ' ' + token.capitalize()
        return ' ' + token

    def _get_random_token(self, key):
        random_number = random.random()
        for token_id, chance in self.probability[key].items():
            if random_number < chance:
                return self.id_to_word[token_id]
            else:
                random_number -= chance
        print(f"ERROR!!!!! {key}\n {self.probability[key].items()}")
        sys.exit(0)

    def _get_random_valid_token(self, key):
        attempts = 100
        while attempts:
            token = self._get_random_token(key)
            if self._is_valid_token(token):
                return token
            attempts -= 1
        assert False, f"Error: no valid tokens found.\nkey: {key}, last tokens: {self.last_tokens_id}"

    def _make_valid_last_tokens_id(self):
        while (len(self.last_tokens_id) > self.depth) or (tuple(self.last_tokens_id) not in self.probability) or\
                not list(filter(lambda token_id: self._is_valid_token(self.id_to_word[token_id]),
                                self.probability[tuple(self.last_tokens_id)].keys())):
            self.last_tokens_id.popleft()

    def _update_punctuation_stack(self, token):
        if token in punctuation.PAIRED_PUNCTUATION:
            if self.stack and self.stack[-1] == punctuation.get_punctuation_pair(token):
                self.stack.pop()
            else:
                self.stack.append(token)

    def _get_generating_step(self, sentence_ending):
        is_step_skipped = False
        if sentence_ending:
            if not self.stack:
                token = sentence_ending
                sentence_ending = None
            else:
                token = punctuation.get_punctuation_pair(self.stack[-1])
        else:
            self._make_valid_last_tokens_id()
            key = () if random.random() < self.uniform_proba else tuple(self.last_tokens_id)
            token = self._get_random_valid_token(key)

            if token in punctuation.SENTENCE_ENDING_PUNCTUATION and self.stack:
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

            self.text += self._get_modifyed_token(token)
            self.last_tokens_id.append(self.word_to_id[token])

            self._update_punctuation_stack(token)
            tokens_generated += 1

    def reset(self):
        self.last_tokens_id = collections.deque()
        self.text = ''
        self.stack = []

    def _add_tokens(self, tokens):
        for token in tokens:
            if token not in self.word_to_id:
                token_id = len(self.word_to_id)
                self.word_to_id[token] = token_id
                self.id_to_word[token_id] = token

    def set_last_tokens_id(self, data):
        tokens = tokens_parser.get_tokens(data)
        self._add_tokens(tokens)
        tokens_id = list(map(lambda token: self.word_to_id[token], tokens))
        self.last_tokens_id = collections.deque(tokens_id)

    def get_probability(self, amount=10):
        self._make_valid_last_tokens_id()
        possible_tokens_id = list(self.probability[tuple(self.last_tokens_id)].items())
        possible_tokens = [(self.id_to_word[token_id], probability) for token_id, probability in possible_tokens_id]
        print(tuple(self.id_to_word[token_id] for token_id in self.last_tokens_id))
        possible_tokens.sort(key=lambda item: item[1], reverse=True)
        return possible_tokens[:amount]

    def set_depth(self, depth):
        self.depth = depth

    def get_text(self):
        return self.text
