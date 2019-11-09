<a target="_blank" rel="noopener noreferrer" href="http://www.montypython.net/sounds/sketches/exparrot.wav"> <img src=https://github.com/Esukhia/pybo/blob/master/pybo_logo.png width=150> </a>

# PYBO - Tibetan NLP in Python
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://black.readthedocs.io/en/stable/)


## Overview

pybo tokenizes Tibetan text into words.

### Basic usage


#### Getting started
Requires to have Python3 installed.

    pip3 install --user pybo

#### Tokenizing a string

```bash
drupchen@drupchen:~$ pybo tok-string "༄༅། །རྒྱ་གར་སྐད་དུ། བོ་དྷི་སཏྭ་ཙརྻ་ཨ་བ་ཏ་ར། བོད་སྐད་དུ། བྱང་ཆུབ་སེམས་དཔའི་སྤྱོད་པ་ལ་འཇུག་པ། །
སངས་རྒྱས་དང་བྱང་ཆུབ་སེམས་དཔའ་ཐམས་ཅད་ལ་ཕྱག་འཚལ་ལོ། །བདེ་གཤེགས་ཆོས་ཀྱི་སྐུ་མངའ་སྲས་བཅས་དང༌། །ཕྱག་འོས་ཀུན་ལའང་གུས་པར་ཕྱག་འཚལ་ཏེ། །བདེ་གཤེགས་
སྲས་ཀྱི་སྡོམ་ལ་འཇུག་པ་ནི། །ལུང་བཞིན་མདོར་བསྡུས་ནས་ནི་བརྗོད་པར་བྱ། །"
Loading Trie... (2s.)
༄༅།_། རྒྱ་གར་ སྐད་ དུ །_ བོ་ དྷི་ སཏྭ་ ཙརྻ་ ཨ་བ་ ཏ་ ར །_ བོད་སྐད་ དུ །_ བྱང་ཆུབ་ སེམས་དཔ འི་ སྤྱོད་པ་ ལ་ འཇུག་པ །_། སངས་རྒྱས་ དང་ བྱང་ཆུབ་
སེམས་དཔའ་ ཐམས་ཅད་ ལ་ ཕྱག་ འཚལ་ ལོ །_། བདེ་གཤེགས་ ཆོས་ ཀྱི་ སྐུ་ མངའ་ སྲས་ བཅས་ དང༌ །_། ཕྱག་འོས་ ཀུན་ ལ འང་ གུས་པ ར་ ཕྱག་ འཚལ་
ཏེ །_། བདེ་གཤེགས་ སྲས་ ཀྱི་ སྡོམ་ ལ་ འཇུག་པ་ ནི །_། ལུང་ བཞིན་ མདོར་བསྡུས་ ནས་ ནི་ བརྗོད་པ ར་ བྱ །_།
```

#### Tokenizing a file
Writes a file of the same name suffixed with `_pybo`

```bash
The file that will be tokenized:
drupchen@drupchen:~$ head text.txt
བཀྲ་ཤི་ས་བདེ་ལེགས་ཕུན་སུམ་ཚོགས། །རྟག་ཏུ་བདེ་བ་ཐོབ་པར་ཤོག། །

drupchen@drupchen:~$ pybo tok-file text.txt
parsing text.txt...
Loading Trie... (2s.)
done

The output file:
drupchen@drupchen:~$ head text_pybo.txt
བཀྲ་ ཤི་ ས་ བདེ་ལེགས་ ཕུན་སུམ་ ཚོགས །_། རྟག་ ཏུ་ བདེ་བ་ ཐོབ་པ ར་ ཤོག །_།
```

### Sorting Tibetan words
```bash
drupchen@drupchen:~$ pybo kakha to-sort.txt
```
The expected input is one word or entry per line in a .txt file. The file will be overwritten.

### FNR - Find and Replace with a list of regexes

```
pybo fnr <in-dir> <regex-file> -o <out-dir> -t <tag>
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

## Maintainance

Build the source dist:

```
rm -rf dist/
python3 setup.py clean sdist
```

and upload on twine (version >= `1.11.0`) with:

```
twine upload dist/*
```

## License

The Python code is Copyright (C) 2019 Esukhia, provided under [Apache 2](LICENSE). 

contributors:
 * [Drupchen](https://github.com/drupchen)
 * [Élie Roux](https://github.com/eroux)
 * [Ngawang Trinley](https://github.com/ngawangtrinley)
 * Joyce Mackzenzie for reworking the logo
