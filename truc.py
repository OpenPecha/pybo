from pathlib import Path
from shutil import copyfile

from bordr import rdr as r
from pybo.rdr.rdr_2_replace_matcher import rdr_2_replace_matcher


def rdr_postprocess(rules, infile, outdir=None, keep=None):
    suffixes = [".DICT", ".INIT", ".RAW", ".RDR", ".sDict"]
    if not outdir:
        outdir = infile.parent
    else:
        outdir = Path(outdir)

    # write adjustment file
    adj_file = outdir / (infile.stem + ".tsv")
    adj_file.write_text(rules, encoding="utf-8-sig")

    # copy files to output directory
    if keep == "all":
        for s in suffixes:
            src = infile.parent / (infile.name + s)
            dst = outdir / (infile.name + s)
            copyfile(src, dst)
    elif keep == "model":
        for s in [".DICT", ".RDR"]:
            src = infile.parent / (infile.name + s)
            dst = outdir / (infile.name + s)
            copyfile(src, dst)
    elif keep is None:
        pass
    else:
        raise SyntaxError("'keep' should either be 'all' or 'model'.")

    # remove temporary files
    for suffix in suffixes:
        Path(infile.parent / (infile.name + suffix)).unlink()


def rdr(infile, outdir=None, keep="model"):
    """

    :param infile:
    :param outdir:
    :param keep: all RDR files if "all", the .RDR and .DICT files if "model", none if None
    :return:
    """
    infile = Path(infile).resolve()

    # run the RDR training
    log = r(str(infile), mode="train", verbose=True)

    # translate to adjustment tsv
    rdr_rules = Path(infile.parent / (infile.name + ".RDR")).read_text(encoding="utf-8-sig")
    rules = rdr_2_replace_matcher(rdr_rules)

    # remove RDR files and copy them if needed
    rdr_postprocess(rules, infile, outdir=outdir, keep=keep)

    return log if log else None


print(rdr("rdr_input.txt", outdir="../", keep="all"))
print()
