# Text-Generator

text-generator supports text based learning and generating new text.

## How it works
In _calculate_probabilities_ mode text-generator analizes text and calculates for every pair of token __t__ and sequence of tokens __s__ (where __s__ is shorter than depth - constant parameter) probability that __t__ is in text right after __s__. In _generate_text_ mode text-generator makes new text using probabilities calculated during studying.

## Usage

It can be launched in two modes.
* calculate_probabilities
  * -h, --help                                _show help message and exit_
  * --input_file INPUT_FILE                   _file to read text from_
  * --probabilities_file PROBABILITIES_FILE   _file to write probabilities to_
  * --depth DEPTH                             _maximum length of the sequence of tokens_
  * --regex REGEX                             _regular expression to identify token_
```shell
$ python3 main.py calculate_probabilities [-h] [--input_file INPUT_FILE] [--probabilities_file PROBABILITIES_FILE] [--depth DEPTH] [--regex REGEX]
```
> example
```shell
$ python3 main.py calculate_probabilities --input_file roadside_picnic.txt --probabilities_file probabilities.txt --depth 3 --regex "\d+"
```

* generate_text
  *  -h, --help                               _show this help message and exit_
  *  --probabilities_file PROBABILITIES_FILE  _file to read probabilities from_
  *  --depth DEPTH                            _maximum length of the sequence of tokens_
  *  --tokens_amount TOKENS_AMOUNT            _length of text to be generated, in tokens_
  *  --output_file OUTPUT_FILE                _file to write text to (by default is set to sys.stdout)_
```shell
$ python3 main.py generate_text [-h] [--probabilities_file PROBABILITIES_FILE] [--depth DEPTH] [--tokens_amount TOKENS_AMOUNT] [--output_file OUTPUT_FILE]
```
> example
```shell
$ python3 main.py generate_text --probabilities_file probabilities.txt --depth 3 --tokens_amount 200
```
