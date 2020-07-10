# coding: utf-8


def pybo_prep(in_str):
    # remove all returns from input
    in_str = in_str.replace("\n", "")
    return in_str


# tokenizing method implemented in cli.py


def get_tag(token, tag_code):
    maps = {"r": "text", "t": "text_cleaned", "p": "pos", "l": "lemma", "s": "sense"}
    try:
        return token[maps[tag_code]]
    except:
        return ""


def pybo_mod(tokens, tag_codes=None):
    """extract text/pos tuples from Token objects"""
    txt_tags = []
    for token in tokens:
        tags = []
        tags.append(token.text)
        # Select and order the tags
        for tag_code in tag_codes:
            tags.append(get_tag(token, tag_code))
        txt_tags.append(tags)
    return txt_tags


def ws2uc(tags):
    """Convert whitespace in raw-text to underscore."""
    tags[0] = tags[0].replace(" ", "_")
    return tags


def pybo_form(tokens, sep=" "):
    """Format in a single string to be written to file"""
    # concatenate text/pos in a single string and replace all in-token spaces by underscores
    out = ["/".join(ws2uc(t)) for t in tokens]
    return sep.join(out)
