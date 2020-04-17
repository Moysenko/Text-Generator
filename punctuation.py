OPEN_BRACKETS = '([{<'
CLOSE_BRACKETS = ')]}>'
SENTENCE_ENDING_PUNCTUATION = '.?!'
PAIRED_PUNCTUATION = OPEN_BRACKETS + CLOSE_BRACKETS + '"\''
VALID_PUNCTUATION_PAIRS = ['?!', '!!', ',-']
PUNCTUATION_PAIR = dict((bracket, CLOSE_BRACKETS[OPEN_BRACKETS.find(bracket)]) if bracket in OPEN_BRACKETS
                        else (bracket, OPEN_BRACKETS[CLOSE_BRACKETS.find(bracket)])
                        for bracket in OPEN_BRACKETS + CLOSE_BRACKETS)
