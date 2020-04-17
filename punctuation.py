OPEN_BRACKETS = '([{<'
CLOSE_BRACKETS = ')]}>'
SENTENCE_ENDING_PUNCTUATION = '.?!'
PAIRED_PUNCTUATION = OPEN_BRACKETS + CLOSE_BRACKETS + '"\''
VALID_PUNCTUATION_PAIRS = ['?!', '!!', ',-']
<<<<<<< HEAD
PUNCTUATION_PAIR = dict((bracket, CLOSE_BRACKETS[OPEN_BRACKETS.find(bracket)]) if bracket in OPEN_BRACKETS
                        else (bracket, OPEN_BRACKETS[CLOSE_BRACKETS.find(bracket)])
                        for bracket in OPEN_BRACKETS + CLOSE_BRACKETS)
=======
PUNCTUATION_PAIR = {CLOSE_BRACKETS[OPEN_BRACKETS.find(bracket)] if bracket in OPEN_BRACKETS
                    else OPEN_BRACKETS[CLOSE_BRACKETS.find(bracket)]
                    for bracket in OPEN_BRACKETS + CLOSE_BRACKETS}
>>>>>>> 0caf20a2f1a488008c85e557b428faa39c5607a6
