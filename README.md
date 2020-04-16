# Text-Generator

text-generator supports text based learning and generating new text.


## How it works
In _calculate_probabilities_ mode text-generator analizes text and calculates for every pair of token __t__ and sequence of tokens __s__ (where __s__ is shorter than depth - constant parameter) probability that __t__ is in text right after __s__. In _generate_text_ mode text-generator makes new text using probabilities calculated during studying.


## Usage

It can be launched in two modes.
* calculate_probabilities
  * -h, --help                                  _show help message and exit_
  * --input\_file INPUT\_FILE                   _file to read text from_
  * --probabilities\_file PROBABILITIES\_FILE   _file to write probabilities to_
  * --depth DEPTH                               _maximum length of the sequence of tokens_
  * --regex REGEX                               _regular expression to identify token_
```shell
$ python3 main.py calculate_probabilities [-h] [--input_file INPUT_FILE] [--probabilities_file PROBABILITIES_FILE] [--depth DEPTH] [--regex REGEX]
```
> example
```shell
$ python3 main.py calculate_probabilities --input_file roadside_picnic.txt --probabilities_file probabilities.txt --depth 3 --regex "\d+"
```

* generate_text
  *  -h, --help                                 _show this help message and exit_
  *  --probabilities\_file PROBABILITIES\_FILE  _file to read probabilities from_
  *  --depth DEPTH                              _maximum length of the sequence of tokens_
  *  --tokens\_amount TOKENS\_AMOUNT            _length of text to be generated, in tokens_
  *  --output\_file OUTPUT\_FILE                _file to write text to (by default is set to sys.stdout)_
  *  --uniform\_proba UNIFORM\_PROBA            *with a probability 1 - uniform\_proba the next token is 
                                                choosing as before, and with a probability uniform_proba 
                                                token is choosing among all tokens*:
```shell
$ python3 main.py generate_text [-h] [--probabilities_file PROBABILITIES_FILE] [--depth DEPTH] [--tokens_amount TOKENS_AMOUNT] [--output_file OUTPUT_FILE] [--uniform_proba UNIFORM_PROBA]
```
> example
```shell
$ python3 main.py generate_text --probabilities_file probabilities.txt --depth 3 --tokens_amount 200 --output_file output.txt --uniform_proba 0.05
```

## Examples of generated text
Text: Peter Pan,  Depth: 2

---

Thus window. Is the hand, it was not meet houses? A her for we shall for fairies. If fly just why hand, it is perfectly over some mothers romp in have into her john, said john. Tink to, house broken test of breeding; once even her. They could sit it are not when though arm age, john said like her. Been fall of back wayward peter cauliflowers dropped time he did it mind. Gallant great red to. It was the right. She meant religion morning, thatblackbeard's of the some mothers also cheek their and and your nearly fellow make! But in but it, she of this before. What on the children, however, can get me the house believe familiar? Shouted slowly colour forth more! Look at are one of executionyou're distinct casually. Wendy presently already in their to go out. And he asleep he said, and it is mrs. Darling always in the old lady while long ago they aside, so, before and that medicine many bump.
