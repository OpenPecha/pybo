from pathlib import Path

from bordr import rdr as r
from pybo.utils.rdr_2_replace_matcher import rdr_2_replace_matcher


def rdr(infile):
    # paths
    infile = Path(infile).resolve()
    rdr_rules = infile.parent / (infile.name + ".RDR")
    adj_file = infile.parent / (infile.stem + ".tsv")

    # RDR
    log = r(str(infile), mode="train", verbose=True)

    # translate to adjustment tsv
    dump = rdr_rules.read_text(encoding="utf-8-sig")
    rules = rdr_2_replace_matcher(dump)

    # write adjustment file
    adj_file.write_text(rules, encoding="utf-8-sig")

    # remove temporary files
    for suffix in [".DICT", ".INIT", ".RAW", ".RDR", ".sDict"]:
        Path(infile.parent / (infile.name + suffix)).unlink()

    return log if log else None

print(rdr("rdr_input.txt"))
print()
