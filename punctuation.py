OPEN_BRACKETS = '([{<'
CLOSE_BRACKETS = ')]}>'
SENTENCE_ENDING_PUNCTUATION = '.?!'
PAIRED_PUNCTUATION = OPEN_BRACKETS + CLOSE_BRACKETS + '"\''
VALID_PUNCTUATION_PAIRS = ['?!', '!!', ',-']
PUNCTUATION_PAIR = {open_bracket: close_bracket for open_bracket, close_bracket in zip(OPEN_BRACKETS, CLOSE_BRACKETS)}+\
                   {close_bracket: open_bracket for close_bracket, open_bracket in zip(CLOSE_BRACKETS, OPEN_BRACKETS)}
