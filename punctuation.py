OPEN_BRACKETS = '([{<"\''
CLOSE_BRACKETS = ')]}>"\''  # brackets should be in same order as their pairs from OPEN_BRACKETS
SENTENCE_ENDING_PUNCTUATION = '.?!'
PAIRED_PUNCTUATION = OPEN_BRACKETS + CLOSE_BRACKETS
VALID_PUNCTUATION_PAIRS = ['?!', '!!', ',-']

PUNCTUATION_PAIR = {}
for openBracket, closeBracket in zip(OPEN_BRACKETS, CLOSE_BRACKETS):  # declaration of PUNCTUATION_PAIR
    PUNCTUATION_PAIR[openBracket] = closeBracket
    PUNCTUATION_PAIR[closeBracket] = openBracket
