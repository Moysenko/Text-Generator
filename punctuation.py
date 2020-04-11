open_brackets = '([{<'
close_brackets = ')]}>'
sentence_ending_punctuation = '.?!'
paired_punctuation = open_brackets + close_brackets + '"\''
valid_punctuation_pairs = ['?!', '!!', ',-']


def get_punctuation_pair(char):
    if char in open_brackets:
        return close_brackets[open_brackets.find(char)]
    if char in close_brackets:
        return open_brackets[close_brackets.find(char)]
    return char
