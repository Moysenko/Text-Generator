import pickle
import argparse
import text_generator
import ngram_probabilities


def _get_probability(probability_file):
    with open(probability_file, "rb") as file:
        probability = ngram_probabilities.NgramProbabilities(probabilities=pickle.load(file),
                                                             id_to_token=pickle.load(file))
    return probability


def _write_text(output_file, text):
    if not output_file:
        print(text)
    else:
        with open(output_file, "w") as file:
            file.write(text)


def _show_help():
    print('''
List of available commands:
    > help            show list of available commands
    > generate x      generate x tokens and add them to text
    > reset           delete text and the tokens history, so the text generating starts from the beginning
    > start "string without brackets"
                      set last used tokens to the entered string
    > show [x]        show x (default: x = 10) most possible tokens
    > depth x         set the depth to x
    > text            show current text
    > exit            write current text and exit
                  ''')


def _interact(generator):
    commands = ["help", "generate", "reset", "start", "show", "depth", "text", "exit"]

    parser = argparse.ArgumentParser(prog='InteractiveGenerator')
    parser.add_argument('query', choices=commands)
    parser.add_argument('args', nargs=argparse.REMAINDER)

    print('Welcome to text generator! Type "help" for help')

    while True:
        query = input('> ').split()
        cmd = parser.parse_args(query)

        try:
            if cmd.query == 'help':
                _show_help()
            elif cmd.query == 'generate':
                generator.add_text(int(cmd.args[0]))
            elif cmd.query == 'reset':
                generator.reset()
            elif cmd.query == 'start':
                generator.set_last_tokens_id(cmd.args)
            elif cmd.query == 'show':
                if cmd.args:
                    print(generator.get_probability(int(cmd.args[0])))
                else:
                    print(generator.get_probability())
            elif cmd.query == 'depth':
                generator.set_depth(int(query[1]))
            elif cmd.query == 'text':
                print(generator.get_text())
            elif cmd.query == 'exit':
                break
        except Exception:
            print('Not valid command. Type "help" for help')


def run_interactive_text_generator(probability_file, depth, output_file, uniform_proba):
    probability = _get_probability(probability_file)
    print('probability initialized')
    generator = text_generator.Generator(probability, depth, uniform_proba)
    print('generator initialized')
    _interact(generator)
    _write_text(output_file, generator.text)
