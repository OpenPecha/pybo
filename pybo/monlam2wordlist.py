import csv
import re

ID = -1

POS_NAMES = ("མིང་ཚིག", "བྱ་ཚིག", "བྱེད་ཚིག", "གྲོགས་ཚིག")


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
            if i == estimated_n_pos - 2:  # if last chunk, check for pos
                found_next_pos = False
                for pos_name in POS_NAMES:
                    next_pos_char_start_idx = chunk_containing_pos.find(pos_name)
                    if next_pos_char_start_idx != -1:
                        found_next_pos = True
                        pos_content = chunk_containing_pos[
                            : next_pos_char_start_idx - 1
                        ]
                        pos_list.append((pos, pos_content))
                        pos, pos_content = get_single_pos(
                            chunk_containing_pos[next_pos_char_start_idx:]
                        )
                        pos_list.append((pos, pos_content))
                if not found_next_pos:
                    pos_list.append((pos, chunk_containing_pos))
            else:
                next_pos_char_start_idx = chunk_containing_pos.rfind(" ")
                pos_content = chunk_containing_pos[:next_pos_char_start_idx]
                pos_list.append((pos, pos_content))
                pos = chunk_containing_pos[next_pos_char_start_idx + 1 :]

    return pos_list


def parse_attrs(text):
    pos_list = get_pos_list(text)
    print(pos_list)


def monlam2wordlist(rows):
    word_list_rows = []
    for row in rows:
        *_, form, result = row
        attrs = parse_attrs(result)
        print(row, attrs)
    return word_list_rows


def dump_tsv(rows, out_path):
    with open(out_path, "w") as csv_file:
        writer = csv.writer(csv_file, delimiter="\t")
        writer.writerows(rows)
