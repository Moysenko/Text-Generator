import pickle
import text_generator


def _get_probability(probability_file):
    with open(probability_file, "rb") as file:
        probability = pickle.load(file)
        print('probability loaded')
        id_to_word = pickle.load(file)
        print('id_to_word loaded')
    return probability, id_to_word


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
    commands = {"help": 1,
                "generate": 2,
                "reset": 1,
                "start": 1,
                "show": 1,
                "depth": 2,
                "text": 1,
                "exit": 1}

    print('Welcome to text generator! Type "help" for help')

    while True:
        query = input('> ').split()
        if not query or query[0] not in commands or len(query) < commands[query[0]]:
            print('Not valid command. Type "help" for help')
            continue

        if query[0] == 'help':
            _show_help()
        elif query[0] == 'generate':
            generator.add_text(int(query[1]))
        elif query[0] == 'reset':
            generator.reset()
        elif query[0] == 'start':
            generator.set_last_tokens_id(query[1:])
        elif query[0] == 'show':
            if len(query) > 1:
                print(generator.get_probability(int(query[1])))
            else:
                print(generator.get_probability())
        elif query[0] == 'depth':
            generator.set_depth(int(query[1]))
        elif query[0] == 'text':
            print(generator.get_text())
        elif query[0] == 'exit':
            break


def generate(probability_file, depth, tokens_amount, output_file, uniform_proba):
    probability, id_to_word = _get_probability(probability_file)
    print('probability initialized')
    generator = text_generator.generator(probability, id_to_word, depth, uniform_proba)
    print('generator initialized')
    _interact(generator)
    _write_text(output_file, generator.text)
