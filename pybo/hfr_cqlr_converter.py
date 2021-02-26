import re
from pathlib import Path

cql2hfr_tag = {
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


def cqlr2hfr(cqlr_string):
    """Convert corpus queery language(cql) rules to human friendly rules(hfr) which has UDPOS in Tibetan.

    Args:
        cql_string (str): corpus queery language rules

    Returns:
        str: human friendly rules(in Tibetan language)
    """
    hfr_string = cqlr_string
    for cql_tag, hfr_tag in cql2hfr_tag.items():
        hfr_string = hfr_string.replace(cql_tag, hfr_tag)
    return hfr_string


def hfr2cqlr(hfr_string):
    """Convert human friendly rules(hfr) to corpus queery language rules format.

    Args:
        hfr_string (str): Human friendly rules(hfr)

    Returns:
        str: Corpus queery language(cql) rules format.
    """
    cql_string = hfr_string
    for cql_tag, hfr_tag in cql2hfr_tag.items():
        cql_string = cql_string.replace(hfr_tag, cql_tag)
    return cql_string
