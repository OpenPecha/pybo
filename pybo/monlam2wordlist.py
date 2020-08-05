import csv
import re

from botok import Text

ID = -1

POS_NAMES = (" མིང་ཚིག ", " བྱ་ཚིག ", " བྱེད་ཚིག ", " གྲོགས་ཚིག ")


class cols:
    ID = "ID"
    FORM = "Form"
    LEMMA = "Lemma"
    MON_POS = "MonPOS"
    MON_FEATURE = "MonFeature"
    MON_TAG = "MonTag"
    POS = "POS"
    FEATURE = "Feature"
    MORPH = "Morph"
    SENSE_TAG = "SenseTag"
    DEFINITION = "Definition"
    EXAMPLE = "Example"


def create_word(
    form,
    lemma,
    mon_pos=None,
    mon_feature=None,
    mon_tag=None,
    pos=None,
    feature=None,
    morph=None,
    sense_tag=None,
    definition=None,
    example=None,
):
    global ID
    ID += 1
    return {
        "ID": ID,
        "Form": form,
        "Lemma": lemma,
        "MonPOS": mon_pos,
        "MonFeature": mon_feature,
        "MonTag": mon_tag,
        "POS": pos,
        "Feature": feature,
        "Morph": feature,
        "SenseTag": sense_tag,
        "Definition": definition,
        "Example": example,
    }


def csv_loader(path):
    with open(path, "r") as csv_file:
        reader = csv.reader(csv_file)
        for i, row in enumerate(reader):
            if i == 0:
                continue
            yield row


def get_single_pos(chunk_containing_pos):
    """Return only first pos and it's content."""
    pos_char_end_idx = chunk_containing_pos.find(" ")
    pos = chunk_containing_pos[:pos_char_end_idx]
    pos_content = chunk_containing_pos[(pos_char_end_idx + 1) :]
    return pos, pos_content


def find_all_remaining_pos(chunk):
    """Return all pos position and it's length.

    Return:
        pos_start_idxs (list): [(pos_start_idx, len(pos_name)), ...] sorted on pos_start_idx.

    """
    pos_start_idxs = []
    pos_found = False
    for pos_name in POS_NAMES:
        pos_found = True
        pos_start_idx = chunk.find(pos_name)
        if pos_start_idx != -1:
            pos_start_idxs.append((pos_start_idx, len(pos_name)))
    if pos_found:
        pos_start_idxs.append((len(chunk), 0))
    return sorted(pos_start_idxs, key=lambda x: x[0])


def get_pos_list(text):
    """Parse pos and it's content (mon_tags, definitions) in string.

    Returns:
        post_list (list): [(pos, pos_content), ...]
    """

    pos_list = []
    chunks_containing_pos = text.split(" 1. ")
    estimated_n_pos = len(chunks_containing_pos)
    if estimated_n_pos == 1:  # one_pos_one_sense
        chunk_containing_pos = chunks_containing_pos[0].strip()
        pos, pos_content = get_single_pos(chunk_containing_pos)
        pos_list.append((pos, pos_content))
    elif estimated_n_pos == 2:  # one_pos_multi_senses
        pos, pos_content = chunks_containing_pos
        pos_list.append((pos, pos_content))
    else:  # multi_pos_multi_senses
        pos = chunks_containing_pos[0]
        for i, chunk_containing_pos in enumerate(chunks_containing_pos[1:]):
            if i == estimated_n_pos - 2:  # if last chunk, check for all pos
                new_chunk_start = 0
                next_pos_start_idxs = find_all_remaining_pos(chunk_containing_pos)
                for next_pos_start_idx, pos_name_len in next_pos_start_idxs:
                    pos_content = chunk_containing_pos[
                        new_chunk_start:next_pos_start_idx
                    ]
                    pos_list.append((pos, pos_content))
                    pos = chunk_containing_pos[
                        next_pos_start_idx : next_pos_start_idx + pos_name_len
                    ].strip()
                    new_chunk_start = next_pos_start_idx + pos_name_len
                if not next_pos_start_idxs:
                    pos_list.append((pos, chunk_containing_pos))
            else:
                next_pos_start_idx = chunk_containing_pos.rfind(" ")
                pos_content = chunk_containing_pos[:next_pos_start_idx]
                pos_list.append((pos, pos_content))
                pos = chunk_containing_pos[next_pos_start_idx + 1 :]

    return pos_list


def get_definition_list(pos_list):
    """Parse definitions from pos_content.

    Returns:
        definition_list (list): [(pos, definition-content), ...]

    """
    definition_list = []
    for pos, pos_content in pos_list:
        for definition_content in re.split(r" \d\. ", pos_content):
            definition_list.append((pos, definition_content))
    return definition_list


def get_tag_list(definition_list):
    """Parse monlam tag from definition content.

    Returns:
        tag_list (list): [(pos, tag, definition), ...]
    """

    def parse_tag(text):
        if text[0] != "༡":
            return "", text
        tag_end_idx = text.find(" ")
        tag = text[:tag_end_idx]
        definition = text[tag_end_idx + 1 :]
        return tag, definition

    tag_list = []
    for pos, definition_content in definition_list:
        tag, definition = parse_tag(definition_content)
        tag_list.append((pos, tag, definition))
    return tag_list


def get_sense_tag_list(tag_list):
    """Parse sense from definition.

    Sense here the first word of the given definition.

    Returns:
        sense_tag_list (list): [(pos, tag, sense_tag, definition), ...]

    """

    def get_first_segment(text, delimiter=" "):
        seg_idx = text.find(delimiter)
        if seg_idx == -1:
            return text
        return text[:seg_idx]

    sense_tag_list = []
    for *pos_and_tag, definition in tag_list:
        first_segment = get_first_segment(definition)
        tokenized_segment = Text(first_segment).tokenize_words_raw_text
        sense = get_first_segment(tokenized_segment)
        sense_tag_list.append((*pos_and_tag, sense, definition))
    return sense_tag_list


def get_example_list(sense_tag_list):
    """Parse example from the definition."""

    def parse_example(text, example_tag="དཔེར་ན།"):
        example_start_idx = text.rfind(example_tag)
        if example_start_idx == -1:
            return text, ""
        definition = text[:example_start_idx].strip()
        example = text[example_start_idx + len(example_tag) :].strip()
        return definition, example

    example_list = []
    for *pos_tag_sense, definition in sense_tag_list:
        definition, example = parse_example(definition)
        example_list.append((*pos_tag_sense, definition, example))
    return example_list


def parse_attrs(form, text_containing_attrs):
    pos_list = get_pos_list(text_containing_attrs)
    definition_list = get_definition_list(pos_list)
    tag_list = get_tag_list(definition_list)
    sense_tag_list = get_sense_tag_list(tag_list)
    example_list = get_example_list(sense_tag_list)
    return example_list


def monlam2wordlist(rows):
    word_list_rows = []
    for row in rows:
        *_, form, result = row
        attrs = parse_attrs(form, result)
        print(row, attrs)
    return word_list_rows


def dump_tsv(rows, out_path):
    with open(out_path, "w") as csv_file:
        writer = csv.writer(csv_file, delimiter="\t")
        writer.writerows(rows)
