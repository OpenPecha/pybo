from pathlib import Path

from pybo.rdr.rdr_2_replace_matcher import rdr_2_replace_matcher


def test_suffix_bug():
    dump = Path("./resources/rdr_rules.txt").read_text()
    rules = rdr_2_replace_matcher(dump)
    print()
