import collections

def _default_dict_with_int_constructor():
    return collections.defaultdict(int)

class NgramProbabilities:
    def _get_D(self, frequences):
        N12 = [0, 0]
        for endings in frequences.values():
            count = sum(endings.values())
            if 1 <= count <= 2:
                N12[count - 1] += 1
        D = N12[0] / (N12[0] + 2 * N12[1]) if N12[0] + N12[1] > 0 else 0
        return D

    def _calc_reversed_pairs(self, frequences, word_to_id):
        pairs = collections.defaultdict(int)
        for value in frequences.values():
            for key in value.keys():
                pairs[word_to_id[key]] += 1
        return pairs

    def _calc_words_id(self, words):
        word_to_id = collections.defaultdict(int)
        id_to_word = list(words)
        for word_id, word in enumerate(words):
            word_to_id[word] = word_id
        return word_to_id, id_to_word

    def _get_deque_id(self, deque, word_to_id):
        return tuple(word_to_id[word] for word in deque)

    def _calc_ngrams(self, frequences, depth):
        pairs = self._calc_reversed_pairs(frequences[1], self.word_to_id)
        total_pairs = sum(pairs.values())

        counter = 0
        for n in range(1, depth + 1):
            D = self._get_D(frequences[n])
            for ngram, endings in frequences[n].items():
                total = sum(endings.values())
                alpha = D * len(endings) / total
                ngram_id = self._get_deque_id(ngram, self.word_to_id)
                for token in self.probabilities[()].keys():
                    first_part = max(endings[self.id_to_word[token]] - D, 0) / total
                    if n == 1:  # bigram
                        Pkn = pairs[token] / total_pairs
                    else:  # n-gram
                        Pkn = self.probabilities[ngram_id[1:]][token]
                    self.probabilities[ngram_id][token] = first_part + alpha * Pkn
                    counter += 1

    def __init__(self, frequences = None, depth = None, probabilities = None, id_to_word = None):
        if frequences:
            self.probabilities = collections.defaultdict(_default_dict_with_int_constructor)

            self.word_to_id, self.id_to_word = self._calc_words_id(frequences[0][()].keys())

            # calc for 0-gram
            self.probabilities[()] = collections.defaultdict(int, [(self.word_to_id[token], frequence)
                                                                   for token, frequence in frequences[0][()].items()])
            total = sum(self.probabilities[()].values())
            for token in self.probabilities[()]:
                self.probabilities[()][token] /= total

            print(len(self.probabilities[()]))

            self._calc_ngrams(frequences, depth)
        else:
            self.probabilities = probabilities
            self.id_to_word = id_to_word
            self.word_to_id = {word: word_id for word_id, word in self.id_to_word.items()}

    def get_ngram_endings(self, ngram):
        return [(self.id_to_word[token_id], probability)
                for token_id, probability in self.probabilities[ngram].items()]

    def _add_tokens(self, tokens):
        for token in tokens:
            if token not in self.word_to_id:
                token_id = len(self.word_to_id)
                self.word_to_id[token] = token_id
                self.id_to_word[token_id] = token