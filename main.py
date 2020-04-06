import argparse
import calculate_probabilities
import generate_text

parser = argparse.ArgumentParser(prog='TextGen',
                                 description='Text generator based on probability of words combinations.')

subparsers = parser.add_subparsers(help='In case mode is set to "calculate_probabilities", \
                    TextGen calculates probabilities of n-grams based on a text passed to the program. \
                    Otherwise, TextGen generates text using calculated probabilities',
                                   dest='mode')

subparser_calculate_probabilities = subparsers.add_parser('calculate_probabilities')
subparser_generate_text = subparsers.add_parser('generate_text')

subparser_calculate_probabilities.add_argument('--input_file', help='file to read text from')
subparser_calculate_probabilities.add_argument('--probabilities_file', help='file to write probabilities to')
subparser_calculate_probabilities.add_argument('--depth', type=int, help='maximum length of the sequence of tokens')

subparser_generate_text.add_argument('--probabilities_file', help='file to read probabilities from')
subparser_generate_text.add_argument('--depth', type=int, help='maximum length of the sequence of tokens')
subparser_generate_text.add_argument('--tokens_amount', type=int, help='length of text to be generated, in tokens')
subparser_generate_text.add_argument('--output_file', default='to console',
                                     help='file to write text to (by default is set to sys.stdout)')

args = parser.parse_args()

if args.mode == 'calculate_probabilities':
    calculate_probabilities.calculate(args.input_file, args.probabilities_file, args.depth)
else:
    generate_text.generate(args.probabilities_file, args.depth, args.tokens_amount, args.output_file)
