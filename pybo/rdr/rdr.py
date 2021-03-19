# coding: utf-8
from pathlib import Path
from shutil import copyfile

from bordr import rdr as r

from .rdr_2_replace_matcher import rdr_2_replace_matcher

from pybo.hfr_cqlr_converter import cqlr2hfr


def rdr_postprocess(rules, infile, outdir=None, keep="model"):
    suffixes = [".DICT", ".INIT", ".RAW", ".RDR", ".sDict"]
    if not outdir:
        outdir = infile.parent.parent
    else:
        outdir = Path(outdir)

    # write adjustment rules file
    adj_file = outdir / (infile.stem + "_rules.tsv")
    adj_file.write_text(rules, encoding="utf-8-sig")

    # copy files to output directory
    for s in suffixes:
        if keep == "all":
            src = infile.parent / (infile.name + s)
            dst = outdir / (infile.name + s)
            if src != dst:
                copyfile(src, dst)
                Path(infile.parent / (infile.name + s)).unlink()
        elif keep == "model":
            if s in [".DICT", ".RDR"]:
                src = infile.parent / (infile.name + s)
                dst = outdir / (infile.name + s)
                if src != dst:
                    copyfile(src, dst)
                    Path(infile.parent / (infile.name + s)).unlink()
            else:
                Path(infile.parent / (infile.name + s)).unlink()
        elif keep == "none":
            Path(infile.parent / (infile.name + s)).unlink()
        else:
            raise SyntaxError("'keep' should either be 'all', 'model' or 'none'.")


def rdr(infile, outdir=None, keep="model", type="cql"):
    """

    :param infile: file to process. should be a POS tagged file
    :param outdir: optional. should be the output directory
    :param keep: all RDR files if "all", the .RDR and .DICT files if "model", none if None
    :return: RDR's log
    """
    infile = Path(infile).resolve()

    # run the RDR training
    log = r(str(infile), mode="train", verbose=True)

    # translate to adjustment tsv
    rdr_rules = Path(infile.parent / (infile.name + ".RDR")).read_text(
        encoding="utf-8-sig"
    )
    rules = rdr_2_replace_matcher(rdr_rules)
    if type is not "cql":
        rules = cqlr2hfr(rules)
    # remove RDR files and copy them if needed
    rdr_postprocess(rules, infile, outdir=outdir, keep=keep)

    return log if log else None
