import re
from pathlib import Path

cqlr = """
[pos="DET" & སུ་] [pos="SCONJ"]	2	=	[pos="ADP"]
["སུ་"] [pos="PRON"] ["ནས་" & pos="SCONJ"]	3	=	[pos="SCONJ"]
"""

cql_hfr_tag = {
    '"ADJ"': "རྒྱན",
    '"ADP"': "སྦྱོར",
    '"ADV"': "བསྣན",
    '"AUX"': "གྲོགས",
    '"CCONJ"': "སྦྲེལ",
    '"DET"': "ངེས",
    '"INTJ"': "འབོད",
    '"NOUN"': "མིང",
    '"NUM"': "གྲངས",
    '"PRON"': "ཚབ",
    '"PROPN"': "ཁྱད",
    '"PUNCT"': "ཚེག",
    '"SCONJ"': "ལྟོས",
    '"VERB"': "བྱ",
    '"PART"': "རོགས",
    "pos=": "གཤིས=",
    "lemma=": "མ=",
    "sense=": "དོན=",
    "&": "༈",
    "[": "༺",
    "]": "༻",
}


def cqlr2hfr(cqlr):
    """Convert corpus queery language(cql) result to human friendly rule(hfr) which has UDPOS in Tibetan.

    Args:
        cql_result (str): corpus queery language result

    Returns:
        str: human friendly rule(in Tibetan language)
    """
    hfr_result = cql_result
    for cql_tag, hfr_tag in cql_hfr_tag.items():
        hfr_result = hfr_result.replace(cql_tag, hfr_tag)
    return hfr_result


def hfr2cqlr(hfr):
    """Convert human friendly rules(hfr) to corpus queery language result format.

    Args:
        hfr_result (str): Human friendly rules(hfr)

    Returns:
        str: Corpus queery language(cql) result format.
    """
    cql_result = hfr_result
    for cql_tag, hfr_tag in cql_hfr_tag.items():
        cql_result = cql_result.replace(hfr_tag, cql_tag)
    return cql_result


if __name__ == "__main__":
    cql_result = Path("./cql/cql.txt").read_text(encoding="utf-8")
    hfr_result = parse_cql(cql_result)
    Path("./hfr_result.txt").write_text(hfr_result, encoding="utf-8")
    Path("./cql_result.txt").write_text(parse_hfr(hfr_result), encoding="utf-8")
