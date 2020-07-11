# coding: utf-8
import botok


def get_chunks(raw_string):
    chunker = botok.Chunks(raw_string)
    chunks = chunker.make_chunks()
    chunks = chunker.get_readable(chunks)
    return chunks


def shelve_info(chunks):
    shelved = []
    clean_chunks = []

    syl_count = 0
    for i, chunk in enumerate(chunks):
        marker, text = chunk
        if marker == "TEXT" or marker == "PUNCT":
            syl_count += 1

        # 2.a. extract transparent chars
        # TODO: adapt to also include \t as transparent char
        if "\n" in text:
            # remove transparent char
            text = text.replace("\n", "")
            index = (syl_count, "\n")

            shelved.append(index)
            clean_chunks.append((marker, text))

        # 2.b. extract any non-bo chunk
        elif marker != "TEXT" and marker != "PUNCT":
            index = (syl_count, text)
            shelved.append(index)

        else:
            clean_chunks.append(chunk)

    return clean_chunks, shelved


def pybo_prep(in_str):
    # 1. get chunks
    chunks = get_chunks(test)

    # 2. shelve needed info
    chunks, shelved = shelve_info(chunks)

    # 3. tokenize
    str_for_botok = "".join([c[1] for c in chunks])

    return str_for_botok


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
