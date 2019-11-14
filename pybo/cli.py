from pathlib import Path
from shutil import rmtree

import click
from botok import Text, __version__, WordTokenizer, expose_data
from pybo import get_regex_pairs, batch_apply_regex, bo_sorted
from pybo import pybo_prep, pybo_mod, pybo_form

from .utils.rdr_2_replace_matcher import rdr_2_replace_matcher


def prepare_folder(main=None, custom=None, overwrite=False):
    profile = "GMD"
    # 1. MAIN PROFILE
    if not main:
        # for better Windows support:
        # https://stackoverflow.com/questions/6227590/finding-the-users-my-documents-path/6227623#6227623
        main = Path.home() / "Documents/pybo/main"
    else:
        main = Path(main)
    main.mkdir(parents=True, exist_ok=True)

    if overwrite:
        rmtree(main, ignore_errors=True)
        main.mkdir()

    try:
        expose_data(main, profile=profile)
    except IOError:
        click.echo('using the existing data in "Documents/pybo/main/"')

    # 2. CUSTOM PROFILE
    if not custom:
        custom = Path.home() / "Documents/pybo/custom"
    else:
        custom = Path(custom)
    custom.mkdir(exist_ok=True)
    for dir in [
        "adjustment",
        "entry_data",
        "words_bo",
        "words_non_inflected",
        "words_skrt",
    ]:
        Path(custom / dir).mkdir(exist_ok=True)

    return main, custom


@click.group()
@click.version_option(__version__)
def cli():
    pass


# Tokenize file
@cli.command()
@click.argument("input-dir", type=click.Path(exists=True))
@click.argument("output-dir", type=click.Path(exists=True))
@click.option("-p", type=click.Path(exists=True), help="main-profile path")
@click.option(
    "-p2",
    multiple=True,
    type=(click.Path(exists=True), click.Path(exists=True)),
    help="paths: main-profile, custom-profile",
)
@click.option("-o", "--overwrite", is_flag=True)
def tok(**kwargs):
    input_dir = Path(kwargs["input_dir"])
    output_dir = Path(kwargs["output_dir"])
    p = kwargs["p"]
    p2 = kwargs["p2"]
    overwrite = kwargs["overwrite"]

    # prepare folder folder to receive all the botok files
    if p and p2:
        click.echo(
            "Choose either -p or -p2 for the tokenizer's profiles, not both\nExiting"
        )
        exit(1)

    if p:
        main, custom = prepare_folder(p, overwrite=overwrite)
        click.echo("main profile: " + p)
    elif p2:
        main, custom = prepare_folder(p2[0][0], p2[0][1], overwrite=overwrite)
        click.echo("main/custom profiles: " + str(p2))
    else:
        main, custom = prepare_folder(overwrite=overwrite)
        click.echo("using default profile")

    wt = WordTokenizer(
        tok_profile=main,
        tok_modifs=custom,
        tok_mode="custom",
        adj_profile=main,
        adj_modifs=custom,
        adj_mode="custom",
        conf_path=main.parent,
    )

    def pybo_tok(in_str):
        return wt.tokenize(in_str)

    for f in input_dir.glob("*.txt"):
        text = Text(f, output_dir / f.name)
        text.custom_pipeline(pybo_prep, pybo_tok, pybo_mod, pybo_form)


# Tokenize string
@cli.command()
@click.argument("string")
def tok_string(**kwargs):
    t = Text(kwargs["string"])
    click.echo(t.tokenize_words_raw_lines)


# rdr_2_replace_matcher
@cli.command()
@click.argument("infile", type=click.Path(exists=True))
def rdr2repl(**kwargs):
    infile = Path(kwargs["infile"])
    outfile = infile.parent / (infile.stem + ".yaml")
    dump = infile.read_text(encoding="utf-8-sig")
    processed = rdr_2_replace_matcher(dump)
    outfile.write_text(processed, encoding="utf-8-sig")


# sort in the Tibetan order
@cli.command()
@click.argument("infile", type=click.Path(exists=True))
def kakha(**kwargs):
    infile = Path(kwargs["infile"])
    words = infile.read_text(encoding="utf-8-sig").split()
    words = bo_sorted(words)
    infile.write_text("\n".join(words), encoding="utf-8-sig")


# FNR - Find and Replace with a list of regexes
@cli.command()
@click.argument("in-dir", type=click.Path(exists=True))
@click.argument("regex-file", type=click.Path(exists=True))
@click.option("-o", "--out-dir", type=click.Path())
@click.option("-t", "--tag")
def fnr(**kwargs):
    # get the args
    indir = Path(kwargs["in_dir"])
    regex_file = Path(kwargs["regex_file"])
    out_dir = Path(kwargs["out_dir"]) if kwargs["out_dir"] else None

    if not indir.is_dir():
        click.echo("IN_DIR should be a folder, not a file.\nexiting...")
        exit(1)

    # optional out file tag
    tag = kwargs["tag"] if kwargs["tag"] else regex_file.stem

    # generate rules
    rules = get_regex_pairs(regex_file.open(encoding="utf-8-sig").readlines())

    # apply on each file, prefixing each one with the regex filename
    for f in indir.rglob("*.txt"):
        if not f.stem.startswith("_"):
            string = f.read_text(encoding="utf-8-sig")
            out = batch_apply_regex(string, rules)
            name = f"_{tag}_" + f.name
            if out_dir:
                Path(out_dir).mkdir(parents=True, exist_ok=True)
                outfile = out_dir / name
            else:
                outfile = f.parent / name
            outfile.write_text(out, encoding="utf-8-sig")


if __name__ == "__main__":
    cli()
