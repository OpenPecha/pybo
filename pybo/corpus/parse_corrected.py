# coding: utf-8
import re
from .word_cleanup import word_cleanup
from ..utils.profile_entries import profile_entries

# from ..utils.bo_sorted import bo_sorted


def parse_corrected(in_str):
    # prepare string: replace returns and tabs and multiple spaces by a single space
    in_str = in_str.replace("\n", " ").replace("\t", " ")
    in_str = re.sub(r"\s+", " ", in_str)

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


def extract_new_entries(in_str, profile_path):
    entries = profile_entries(profile_path)

    # parse input
    parsed = parse_corrected(in_str)

    # generate content, without duplicates
    entry_data = []
    for p in parsed:
        word = p[0]
        e_d = "\t".join(p)
        if (word not in entries or e_d not in entries[word]) and e_d not in entry_data:
            entry_data.append(e_d)

    # sort both lists
    # words = bo_sorted(words)
    # entry_data = bo_sorted(entry_data)
    entry_data = sorted(entry_data)
    entry_data = ["# form	pos	lemma	sense	freq"] + entry_data

    return "\n".join(entry_data)
