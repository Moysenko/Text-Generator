OPEN_BRACKETS = '([{<'
CLOSE_BRACKETS = ')]}>'
SENTENCE_ENDING_PUNCTUATION = '.?!'
PAIRED_PUNCTUATION = OPEN_BRACKETS + CLOSE_BRACKETS + '"\''
VALID_PUNCTUATION_PAIRS = ['?!', '!!', ',-']


def get_punctuation_pair(char):
    if char in OPEN_BRACKETS:
        return CLOSE_BRACKETS[OPEN_BRACKETS.find(char)]
    if char in CLOSE_BRACKETS:
        return OPEN_BRACKETS[CLOSE_BRACKETS.find(char)]
    return char
