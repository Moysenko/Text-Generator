# Text-Generator

text-generator supports text based learning and generating new text.

## How it works
In _calculate_probabilities_ mode text-generator analizes text and calculates for every pair of token __t__ and sequence of tokens __s__ (where __s__ is shorter than depth - constant parameter) probability that __t__ is in text right after __s__. In _generate_text_ mode text-generator makes new text using probabilities calculated during studying.

## Usage

It can be launched in two modes.
* calculate_probabilities
  *  -h, --help                               show help message and exit
  * --input_file INPUT_FILE                   file to read text from
  * --probabilities_file PROBABILITIES_FILE   file to write probabilities to
  * --depth DEPTH                             maximum length of the sequence of tokens
```shell
$ python3 main.py calculate_probabilities [-h] [--input_file INPUT_FILE] [--probabilities_file PROBABILITIES_FILE] [--depth DEPTH]
```
> example
```shell
$ python3 main.py calculate_probabilities --input_file roadside_picnic.txt --probabilities_file probabilities.txt --depth 3
```

* generate_text
  *  -h, --help                               show this help message and exit
  *  --probabilities_file PROBABILITIES_FILE  file to read probabilities from
  *  --depth DEPTH                            maximum length of the sequence of tokens
  *  --tokens_amount TOKENS_AMOUNT            length of text to be generated, in tokens
  *  --output_file OUTPUT_FILE                file to write text to (by default is set to sys.stdout)
```shell
$ python3 main.py generate_text [-h] [--probabilities_file PROBABILITIES_FILE] [--depth DEPTH] [--tokens_amount TOKENS_AMOUNT] [--output_file OUTPUT_FILE]
```
> example
```shell
$ python3 main.py generate_text --probabilities_file probabilities.txt --depth 3 --tokens_amount 200
```
