# Text-Generator

text-generator supports text based learning and generating new text.

## How it works
In _calculate_probabilities_ mode text-generator analizes text and calculates for every pair of token __t__ and 
sequence of tokens __s__ (where __s__ is shorter than **depth** - constant parameter) probability that __t__ is in text right
after __s__. In _generate_text_ mode text-generator makes new text using probabilities calculated during studying.\
Kneser-Ney smoothing is added to make generated text more realistic


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
  *  --output\_file OUTPUT\_FILE                _file to write text to (by default is set to sys.stdout)_
  *  --uniform\_proba UNIFORM\_PROBA            *with a probability 1 - uniform\_proba the next token is 
                                                choosing as before, and with a probability uniform_proba 
                                                token is choosing among all tokens*:
```shell
$ python3 main.py generate_text [-h] [--probabilities_file PROBABILITIES_FILE] [--depth DEPTH] [--output_file OUTPUT_FILE] [--uniform_proba UNIFORM_PROBA]
```
> example
```shell
$ python3 main.py generate_text --probabilities_file probabilities.txt --depth 3 --output_file output.txt --uniform_proba 0.05
```

## Examples of generated text
Text: Peter Pan,  Depth: 3

---

James m. Barrie, sir. A nana to little by his way. Beginning of fairies. Have been there are in the and the. Suitable was up by this time pan lip fly in her! He went again, and when wrote of here was though. Peter was a what not ran to him from peter would bite were and skylights (morgan's skylights like, said doubtfully in by the point he if he in sounded pet off, the floor, looking no pity, the dog to their, lot now (but shadow find round and)). Of the. I know you were huskily boylike, was killed by itisn't it struck, round thebed-post! Do you kill him. Up danger him until at he, and there you could not leapt tucked would spirit room funny address should have mr. Darling was told in of wendy, he said. You could, and it was so small they kings.

