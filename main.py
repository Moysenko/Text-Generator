import argparse

parser = argparse.ArgumentParser(prog='TextGen',
                                 description='Text generator based on probability of words combinations.')

subparsers = parser.add_subparsers(help='In case mode is set to "calculate_probabilities", \
                    TextGen calculates probabilities of n-grams based on a text passed to the program. \
                    Otherwise, TextGen generates text using calculated probabilities')

calculate_probabilities = subparsers.add_parser('calculate_probabilities')
generate_text = subparsers.add_parser('generate_text')

calculate_probabilities.add_argument('--input_file', help='file to read text from')
calculate_probabilities.add_argument('--probabilities_file', help='file to write probabilities to')
calculate_probabilities.add_argument('--depth', help='maximum length of the sequence of tokens')

generate_text.add_argument('--probabilities_file', help='file to read probabilities from')
generate_text.add_argument('--depth', help='maximum length of the sequence of tokens')
generate_text.add_argument('--tokens_amount', help='length of text to be generated, in tokens')
generate_text.add_argument('--output_file', default='to console',
                           help='file to write text to (by default is set to sys.stdout)')

args = parser.parse_args()
