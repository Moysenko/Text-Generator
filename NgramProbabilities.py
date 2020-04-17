import collections

class NgramProbabilities:
    def _get_D(self, frequences):
        N12 = [0, 0]
        for endings in frequences.values():
            count = sum(endings.values())
            if 1 <= count <= 2:
                N12[count - 1] += 1
        D = N12[0] / (N12[0] + 2 * N12[1]) if N12[0] + N12[1] > 0 else 0
        return D

    def _calc_reversed_pairs(self, frequences):
        pairs = collections.defaultdict(int)
        for value in frequences.values():
            for key in value.keys():
                pairs[self.token_to_id[key]] += 1
        return pairs

    def _calc_words_id(self, words):
        word_to_id = collections.defaultdict(int)
        id_to_word = list(words)
        for word_id, word in enumerate(words):
            word_to_id[word] = word_id
        return word_to_id, id_to_word

    def _get_tokens_deque_id(self, deque):
        return tuple(self.token_to_id[word] for word in deque)

    def _get_probability_ngrams_list(self, probabilities):
        probabilities_set = set(probabilities.values())
        probability_ngrams_dict = collections.defaultdict(list)
        for token_id, probability in probabilities.items():
            probability_ngrams_dict[probability].append(token_id)
        probability_ngrams_list = sorted(list(probability_ngrams_dict.items()))
        probability_ngrams_list[-1] = []
        return probability_ngrams_list

    def _get_ngram_probabilities_list(self, ngram_id):
        unused_tokens = set(self.id_to_token)
        ngram_probabilities = []
        for probability, tokens in self.probabilities[ngram_id]:
            if tokens:
                for token in tokens:
                    ngram_probabilities.append((probability, token))
                    unused_tokens.remove(token)
            else:
                for token in unused_tokens:
                    ngram_probabilities.append((probability, token))
        return ngram_probabilities

    def _init_ngrams(self, frequences, depth):
        pairs = self._calc_reversed_pairs(frequences[1])
        total_pairs = sum(pairs.values())

        for n in range(1, depth + 1):
            D = self._get_D(frequences[n])
            for ngram, endings in frequences[n].items():
                total = sum(endings.values())
                alpha = D * len(endings) / total
                ngram_id = self._get_tokens_deque_id(ngram)
                ngram_probabilities = {}
                for token_id, token_probability in self._get_ngram_probabilities_list(ngram_id[1:]):
                    first_part = max(endings[self.id_to_token[token_id]] - D, 0) / total
                    if n == 1:  # bigram
                        Pkn = pairs[token_id] / total_pairs
                    else:  # n-gram
                        Pkn = token_probability
                    ngram_probabilities[token_id] = first_part + alpha * Pkn
                self.probabilities[ngram_id] = self._get_probability_ngrams_list(ngram_probabilities)

                print(f"----------{ngram}---------")
                for probability in set(self.probabilities[()].values()):
                    print(probability, list(self.probabilities[()].values()).count(probability))
                exit(0)
                print("===================================================")

    def _init_0grams(self, frequences):
        zero_gram = dict([(self.token_to_id[token], frequence)
                          for token, frequence in frequences[0][()].items()])
        total = sum(zero_gram.values())
        for token in zero_gram:
            zero_gram[token] /= total
        self.probabilities[()] = self._get_probability_ngrams_list(zero_gram)

    def _init_from_frequences(self, frequences, depth):
        self.probabilities = collections.defaultdict(list)
        self.token_to_id, self.id_to_token = self._calc_words_id(frequences[0][()].keys())
        self._init_0grams(frequences)
        self._init_ngrams(frequences, depth)

    def _init_from_probabilities(self, probabilities, id_to_word):
        self.probabilities = probabilities
        self.id_to_token = id_to_word
        self.token_to_id = {word: word_id for word_id, word in self.id_to_token.items()}

    def __init__(self, frequences=None, depth=None, probabilities=None, id_to_word=None):
        if frequences:
            self._init_from_frequences(frequences, depth)
        else:
            self._init_from_probabilities(probabilities, id_to_word)

    def get_ngram_endings(self, ngram):
        return [(self.id_to_token[token_id], probability)
                for token_id, probability in self._get_ngram_probabilities_list(ngram)]

    def _add_tokens(self, tokens):
        for token in tokens:
            if token not in self.token_to_id:
                token_id = len(self.id_to_token)
                self.id_to_token.append(token)
                self.token_to_id[token] = token_id
