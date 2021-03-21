<a target="_blank" rel="noopener noreferrer" href="http://www.montypython.net/sounds/sketches/exparrot.wav"> <img src=https://github.com/Esukhia/pybo/blob/master/pybo_logo.png width=150> </a>

# PYBO - Tibetan NLP in Python
[![PyPI version](https://badge.fury.io/py/pybo.svg)](https://badge.fury.io/py/pybo)
![Test](https://github.com/Esukhia/pybo/workflows/Test/badge.svg)
![Test Coverage](https://github.com/Esukhia/pybo/workflows/Test%20Coverage/badge.svg)
![Publish](https://github.com/Esukhia/pybo/workflows/Publish/badge.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://black.readthedocs.io/en/stable/)



## Overview

bo tokenizes Tibetan text into words.

### Basic usage


#### Getting started
Requires to have Python3 installed.

    python3 -m pip install pybo

#### Tokenizing a string

```bash
drupchen@drupchen:~$ bo tok-string "༄༅། །རྒྱ་གར་སྐད་དུ། བོ་དྷི་སཏྭ་ཙརྻ་ཨ་བ་ཏ་ར། བོད་སྐད་དུ། བྱང་ཆུབ་སེམས་དཔའི་སྤྱོད་པ་ལ་འཇུག་པ། །
སངས་རྒྱས་དང་བྱང་ཆུབ་སེམས་དཔའ་ཐམས་ཅད་ལ་ཕྱག་འཚལ་ལོ། །བདེ་གཤེགས་ཆོས་ཀྱི་སྐུ་མངའ་སྲས་བཅས་དང༌། །ཕྱག་འོས་ཀུན་ལའང་གུས་པར་ཕྱག་འཚལ་ཏེ། །བདེ་གཤེགས་
སྲས་ཀྱི་སྡོམ་ལ་འཇུག་པ་ནི། །ལུང་བཞིན་མདོར་བསྡུས་ནས་ནི་བརྗོད་པར་བྱ། །"
Loading Trie... (2s.)
༄༅།_། རྒྱ་གར་ སྐད་ དུ །_ བོ་ དྷི་ སཏྭ་ ཙརྻ་ ཨ་བ་ ཏ་ ར །_ བོད་སྐད་ དུ །_ བྱང་ཆུབ་ སེམས་དཔ འི་ སྤྱོད་པ་ ལ་ འཇུག་པ །_། སངས་རྒྱས་ དང་ བྱང་ཆུབ་
སེམས་དཔའ་ ཐམས་ཅད་ ལ་ ཕྱག་ འཚལ་ ལོ །_། བདེ་གཤེགས་ ཆོས་ ཀྱི་ སྐུ་ མངའ་ སྲས་ བཅས་ དང༌ །_། ཕྱག་འོས་ ཀུན་ ལ འང་ གུས་པ ར་ ཕྱག་ འཚལ་
ཏེ །_། བདེ་གཤེགས་ སྲས་ ཀྱི་ སྡོམ་ ལ་ འཇུག་པ་ ནི །_། ལུང་ བཞིན་ མདོར་བསྡུས་ ནས་ ནི་ བརྗོད་པ ར་ བྱ །_།
```

#### Tokenizing a list of files

The command to tokenize a list of files in a directory:
```
bo tok <path-to-directory>
```

For example to tokenize the file `text.txt` in a directory `./document/` with the following content: 
```
བཀྲ་ཤི་ས་བདེ་ལེགས་ཕུན་སུམ་ཚོགས། །རྟག་ཏུ་བདེ་བ་ཐོབ་པར་ཤོག། །
```

I use the command:
```
$ bo tok ./document/
```

...which create a file `text.txt` in a directory `./document_pybo` containing:
```
བཀྲ་ ཤི་ ས་ བདེ་ལེགས་ ཕུན་སུམ་ ཚོགས །_། རྟག་ ཏུ་ བདེ་བ་ ཐོབ་པ ར་ ཤོག །_།
```

### Sorting Tibetan words
```bash
$ bo kakha to-sort.txt
```
The expected input is one word or entry per line in a .txt file. The file will be overwritten.

### FNR - Find and Replace with a list of regexes

```
bo fnr <in-dir> <regex-file> -o <out-dir> -t <tag>
```
`-o` and `-t` are optional

Text files should be UTF-8 plain text files. The regexes should be in the following format:

```
<find-pattern><tab>-<tab><replace-pattern>
```

## Acknowledgements

- **pybo** is an open source library for Tibetan NLP.

We are always open to cooperation in introducing new features, tool integrations and testing solutions.

Many thanks to the companies and organizations who have supported pybo's development, especially:

* [Khyentse Foundation](https://khyentsefoundation.org) for contributing USD22,000 to kickstart the project 
* The [Barom/Esukhia canon project](http://www.barom.org) for sponsoring training data curation
* [BDRC](https://tbrc.org) for contributing 2 staff for 6 months for data curation

- `third_party/rules.txt` is taken from [tibetan-collation](https://github.com/eroux/tibetan-collation/blob/master/implementations/Unicode/rules.txt).

## Contributing
First clone this repo. Create virtual environment and activate it. Then install the dependencies
```bash
$ pip install -e .
$ pip install -r requirements-dev.txt
```

Next, setup up [pre-commit](https://pre-commit.com/) by creating pre-commit git hook
```bash
$ pre-commit install
```
Please, follow [augular commit message format](https://github.com/angular/angular/blob/master/CONTRIBUTING.md#-commit-message-format) for commit message. We have setup [python-semantic-release](https://github.com/relekang/python-semantic-release) to publish [pybo](https://pypi.org/project/pybo/) package automatically based on commit messages.

That's all, Enjoy contributing 🎉🎉🎉

## License

The Python code is Copyright (C) 2019 Esukhia, provided under [Apache 2](LICENSE). 

contributors:
 * [Drupchen](https://github.com/drupchen)
 * [Élie Roux](https://github.com/eroux)
 * [Ngawang Trinley](https://github.com/ngawangtrinley)
 * [Tenzin](https://github.com/10zinten)
 * Joyce Mackzenzie for reworking the logo
