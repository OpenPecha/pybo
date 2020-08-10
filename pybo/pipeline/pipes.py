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
    chunks = get_chunks(in_str)

    # 2. shelve needed info
    chunks, shelved = shelve_info(chunks)
    pybo_form_sep = pybo_form.__defaults__[0]
    pybo_form.__defaults__ = (pybo_form_sep, shelved)

    # 3. tokenize
    str_for_botok = "".join([c[1] for c in chunks])

    return str_for_botok


def get_tag(token, tag_code):
    maps = {"r": "text", "t": "text_cleaned", "p": "pos", "l": "lemma", "s": "sense"}
    try:
        return token[maps[tag_code]]
    except Exception:
        return ""


def pybo_mod(tokens, tag_codes=[]):
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


def n_chunks(token):
    return len([chunk for chunk in token.split("་") if chunk])


def pybo_form(tokens, sep=" ", shelved=None):
    """Format in a single string to be written to file"""
    if not shelved:
        print(shelved)
        out = []
        shelved_idx = 0
        syl_count = 0

        # reinsert shelved tokens
        for token in tokens:
            out.append("/".join(ws2uc(token)))
            syl_count += n_chunks(token[0])
            sheveled_syl_count, shelved_cleaned_chunk = shelved[shelved_idx]
            if "PART" not in token and sheveled_syl_count <= syl_count:
                out.append(ws2uc([shelved_cleaned_chunk])[0])
                shelved_idx += 1

        # add all the remaining sheveld tokens
        if shelved_idx < len(shelved):
            for _, shelved_cleaned_chunk in shelved_cleaned_chunk[shelved_idx:]:
                out.append(ws2uc([shelved_cleaned_chunk]))
    else:
        out = ["/".join(ws2uc(token)) for token in tokens]
    return sep.join(out)
