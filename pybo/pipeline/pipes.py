# coding: utf-8


def pybo_prep(in_str):
    # do nothing
    return in_str


# tokenizing method implemented in cli.py


def pybo_mod(tokens):
    """extract text/pos tuples from Token objects"""
    txt_pos = []
    for t in tokens:
        txt = t.text
        pos = t.pos if t.pos else t.chunk_type
        txt_pos.append((txt, pos))
    return txt_pos


def pybo_form(tokens, sep=" "):
    """Format in a single string to be written to file"""
    # concatenate text/pos in a single string and replace all in-token spaces by underscores
    out = [f'{t[0].replace(" ", "_")}/{t[1]}' for t in tokens]
    return sep.join(out)
