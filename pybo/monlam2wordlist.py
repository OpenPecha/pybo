import csv
import re

ID = -1


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


def parse_attrs(text):
    pass


def monlan2wordlist(rows):
    for row in rows:
        *_, form, result = row
        attrs = parse_attrs(result)
        print(row)
    return word_list_rows


def dump_tsv(rows, out_path):
    with open(out_path, "w") as csv_file:
        writer = csv.writer(csv_file, delimiter="\t")
        writer.writerows(rows)


def main():
    in_path = "../../../tibetan-nlp-dataset/monlam2020.csv"
    out_path = "monlam2020-wordlist.tsv"

    rows = csv_loader(in_path)
    word_list = monlan2wordlist(rows)


#    dump_tsv(word_list, out_path)


if __name__ == "__main__":
    exit(main())
