# coding: utf-8
import re
from .word_cleanup import word_cleanup
from ..utils.bo_sorted import bo_sorted


def parse_corrected(in_str):
    # prepare string: replace returns and tabs and multiple spaces by a single space
    in_str = in_str.replace('\n', ' ').replace('\t', ' ')
    in_str = re.sub(r'\s+', ' ', in_str)

    # parse
    sep_field = "/"
    parsed = []
    for token in in_str.split():
        fields = ["", "", "", "", ""]
        for num, f in enumerate(token.split(sep_field)):
            # cleanup the form and the lemma
            if (num == 0 or num == 2) and f:
                f = word_cleanup(f)
            fields[num] = f
        parsed.append(fields)
    return parsed


def generate_data(in_str):
    # parse input
    parsed = parse_corrected(in_str)

    # generate wordlist and entry_data content, without duplicates
    words = []
    entry_data = []
    for p in parsed:
        word = p[0]
        if word not in words:
            words.append(word)

        e_d = "\t".join(p)
        if e_d not in entry_data:
            entry_data.append(e_d)

    # sort both lists
    words = bo_sorted(words)
    entry_data = bo_sorted(entry_data)
    entry_data = ["# form	pos	lemma	sense	freq"] + entry_data

    return "\n".join(words), "\n".join(entry_data)
