import json
from pathlib import Path
from shutil import rmtree

import click
from bordr import __version__ as bordr__version
from botok import Config, Text, WordTokenizer
from botok import __version__ as botok__version__
from botok import expose_data
from pyewts import VERSION as pyewts__version__
from tibetan_sort import TibetanSort
from tibetan_sort import __version__ as tibetan_sort__version__

from pybo import __version__ as pybo__version__
from pybo.corpus.parse_corrected import extract_new_entries
from pybo.pipeline.pipes import pybo_form, pybo_mod, pybo_prep
from pybo.rdr.rdr import rdr as r
from pybo.rdr.rdr_2_replace_matcher import rdr_2_replace_matcher
from pybo.utils.profile_report import profile_report as p_report
from pybo.utils.regex_batch_apply import batch_apply_regex, get_regex_pairs
from pybo.hfr_cqlr_converter import cqlr2hfr, hfr2cqlr
from pybo.segmentation_rule.pipeline import extract_seg_rule

HOME = Path.home()
DIALECT_PACK_DIR = HOME / "Documents" / "pybo" / "dialect_packs"
DEFAULT_DPACK = "general"
CONFIG_DIR = HOME / ".pybo"
CONFIG_FILE = CONFIG_DIR / "config.json"


@click.group()
@click.version_option(pybo__version__)
def cli():
    pass


@cli.command()
def info():
    click.echo("pybo install path: " + str(Path(__file__).parent.resolve()))
    click.echo("pybo: " + pybo__version__)
    click.echo("botok: " + botok__version__)
    click.echo("pyewts: " + pyewts__version__)
    click.echo("bordr: " + bordr__version)
    click.echo("tibetan_sort: " + tibetan_sort__version__)


def prepare_folder(main=None, custom=None, overwrite=False):
    profile = "POS"
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
    for dir in ["adjustment", "remove", "words", "words_skrt"]:
        Path(custom / dir).mkdir(exist_ok=True)

    return main, custom


def save_config(dialect_pack_path):
    config = {"dialect_pack_path": str(dialect_pack_path)}
    if not CONFIG_DIR.is_dir():
        CONFIG_DIR.mkdir(parents=True)
    json.dump(config, CONFIG_FILE.open("w"))


def load_config():
    if not CONFIG_FILE.is_file():
        return
    else:
        config = json.load(CONFIG_FILE.open())
    return config


# Tokenize file
@cli.command()
@click.argument("input-dir", type=click.Path(exists=True))
@click.option(
    "-t",
    "--tags",
    help="""Select and order the tags. Available tags are:
t-clean_text, p-pos, l-lemma, s-sense.\n
Usage: `-t tpl` will give for every token `<raw-text>/<clean-text>/<pos>/<lemma>`
and will give just `<raw-text>` if tag option is not specified.""",
)
@click.option(
    "-o", type=click.Path(exists=True), help="output dir, default is the input_dir"
)
@click.option("-d", "--dialect-name", type=str, help="official dialect pack name.")
@click.option(
    "-p",
    "--dialect-path",
    type=click.Path(exists=True),
    help="path to the dialect pack",
)
@click.option("-w", "--overwrite", is_flag=True)
@click.option("-r", "--rebuild-trie", is_flag=True)
def tok(**kwargs):
    input_dir = Path(kwargs["input_dir"])
    dialect_name = kwargs["dialect_name"]
    dialect_path = kwargs["dialect_path"]
    # overwrite = kwargs["overwrite"]
    rebuild = kwargs["rebuild_trie"]

    # load botok config
    if dialect_name:
        config = Config(dialect_name=dialect_name)
        save_config(config.dialect_pack_path)
    elif dialect_path:
        config = Config.from_path(dialect_path)
        # config.dialect_pack_path = Path(dialect_pack_path)
        save_config(config.dialect_pack_path)
    else:
        pybo_config = load_config()
        if not pybo_config:
            config = Config()
            save_config(config.dialect_pack_path)
        else:
            dialect_pack_path = pybo_config["dialect_pack_path"]
            config = Config.from_path(dialect_pack_path)

    print(
        f"[INFO] Using `{config.dialect_pack_path.name}` dialect pack for tokenization ..."
    )

    wt = WordTokenizer(config=config, build_trie=rebuild)

    def pybo_tok(in_str):
        return wt.tokenize(in_str)

    # Select and Order the tags
    if kwargs["tags"]:
        pybo_mod.__defaults__ = (list(kwargs["tags"]),)

    if input_dir.is_dir():
        if kwargs["o"] is not None:
            output_dir = Path(kwargs["o"])
        else:
            output_dir = input_dir.parent / (input_dir.name + "_tok")
            output_dir.mkdir(exist_ok=True)
        for f in input_dir.glob("*.txt"):
            out_file = output_dir / (f.stem + "_tok.txt")
            text = Text(f, out_file)
            text.custom_pipeline(pybo_prep, pybo_tok, pybo_mod, pybo_form)
    elif input_dir.is_file():
        input_file = input_dir
        if kwargs["o"] is not None:
            output_dir = Path(kwargs["o"])
        else:
            output_dir = input_file.parent / (input_file.stem + "_tok")
            output_dir.mkdir(exist_ok=True)
        out_file = output_dir / (input_file.stem + "_tok.txt")
        text = Text(input_file, out_file)
        text.custom_pipeline(pybo_prep, pybo_tok, pybo_mod, pybo_form)
    else:
        print("[INFO] Invalid input directory or file!!!")


# Tokenize string
@cli.command()
@click.argument("string")
def tok_string(**kwargs):
    t = Text(kwargs["string"])
    click.echo(t.tokenize_words_raw_lines)


# lists
tag_types = ["pos", "lemma", "sense"]


@cli.command()
@click.argument("input-dir", type=click.Path(exists=True))
@click.option("-t", "--type")
def lists(**kwargs):
    path = Path(kwargs["path"])

    text_string = ""
    for f in path.glob("*.txt"):
        text_string += f.read_text(encoding="utf-8-sig")


# create report for botok profiles
@cli.command()
@click.argument("profile", type=click.Path(exists=True))
def profile_report(**kwargs):
    p_report(kwargs["profile"])


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
    sort = TibetanSort()
    infile = Path(kwargs["infile"])
    words = infile.read_text(encoding="utf-8-sig").split()
    print(f"Sorting {infile.name}")
    words = sort.sort_list(words)
    print(f"{infile.name} is sorted")
    infile.write_text("\n".join(words), encoding="utf-8-sig")


# generate rdr rules
@cli.command()
@click.argument("input", type=click.Path(exists=True))
@click.option("-dp", type=str, help="Dialect pack name, default is general")
@click.option("-k", "--keep", type=str)
@click.option('--type', type=str, help="Type can be either cql which is default type or hfr(Human friendly rule)")
def extract_rules(**kwargs):
    file_or_dir = Path(kwargs["input"])
    dialect_pack_name = kwargs["dp"] if kwargs["dp"] else DEFAULT_DPACK
    keep = "none" if kwargs["keep"] is None else kwargs["keep"]
    type = "cql" if kwargs["type"] is None else kwargs["type"]
    if type == "cql":
        out_dir = DIALECT_PACK_DIR / dialect_pack_name / "adjustments" / "rules"
    else:
        out_dir = DIALECT_PACK_DIR / dialect_pack_name / "hfr_rules"
        out_dir.mkdir(exist_ok=True)

    log = None
    click.echo("[INFO] Extracing adjustments rules ...")
    if file_or_dir.is_dir():
        file = file_or_dir / file_or_dir.name
        with open(file, encoding="utf-8-sig", mode="w") as tmp:
            for f in file_or_dir.glob("*.txt"):
                tmp.write(f.read_text(encoding="utf-8-sig") + " ")
        log = r(file, outdir=out_dir, keep=keep, type=type)
        file.unlink()
    elif file_or_dir.is_file():
        log = r(file_or_dir, out_dir, keep=keep, type=type)
        click.echo(f"[INFO] {file_or_dir} does not exist!")

    click.echo(log)
    click.echo("[INFO] Completed !")
    click.echo(f"[INFO] Added adjustments rules to {dialect_pack_name}")

# generate rdr rules
@cli.command()
@click.argument("input", type=click.Path(exists=True))
@click.option("-dp", type=str, help="Dialect pack name, default is general")
@click.option('--type', type=str, help="Type can be either cql which is default type or hfr(Human friendly rule)")
@click.option("--e", type=int)
def extract_seg_rules(**kwargs):
    rules = ''
    input_path = Path(kwargs["input"])
    dialect_pack_name = kwargs["dp"] if kwargs["dp"] else DEFAULT_DPACK
    type = "cql" if kwargs["type"] is None else kwargs["type"]
    epochs = 3 if kwargs['e'] is None else kwargs['e']
    if type == "cql":
        out_dir = DIALECT_PACK_DIR / dialect_pack_name / "adjustments" / "rules"
    else:
        out_dir = DIALECT_PACK_DIR / dialect_pack_name / "hfr_rules"
        out_dir.mkdir(exist_ok=True)

    click.echo("[INFO] Extracing adjustments rules ...")
    
    if input_path.is_dir():
        print('[ERROR] Invalid file name!!')
    elif input_path.is_file():
        rules += extract_seg_rule(input_path, dialect_pack_name, type, epochs)
        if rules:
            (out_dir / f'{input_path.stem}_rules.tsv').write_text(rules, encoding='utf-8')
        else:
            print('[INFO] No rules found')
        
    click.echo("[INFO] Completed !")
    click.echo(f"[INFO] Added adjustments rules to {dialect_pack_name}")

#convert cql to hfr
@cli.command()
@click.argument("input", type=click.Path(exists=True))
@click.option("-dp", type=str, help="Dialect pack name, default is general")
def convert_cql2hfr(**kwargs):
    cql_path = Path(kwargs['input'])
    dialect_pack_name = kwargs["dp"] if kwargs["dp"] else DEFAULT_DPACK
    hfr_dir = DIALECT_PACK_DIR / dialect_pack_name / "hfr_rules"
    hfr_dir.mkdir(exist_ok=True) 
    hfr_file_path = hfr_dir / (cql_path.stem + ".tsv")
    cql_rules = cql_path.read_text(encoding='utf-8')
    hfr = cqlr2hfr(cql_rules)
    hfr_file_path.write_text(hfr, encoding='utf-8')

#convert hfr to cql
@cli.command()
@click.argument("input", type=click.Path(exists=True))
@click.option("-dp", type=str, help="Dialect pack name, default is general")
def convert_hfr2cql(**kwargs):
    hfr_path = Path(kwargs['input'])
    dialect_pack_name = kwargs["dp"] if kwargs["dp"] else DEFAULT_DPACK
    cql_dir = DIALECT_PACK_DIR / dialect_pack_name / "adjustments" / "rules"
    cql_dir.mkdir(exist_ok = True)
    cql_file_path = cql_dir / (hfr_path.stem + ".tsv")
    hfr = hfr_path.read_text(encoding='utf-8')
    cql = hfr2cqlr(hfr)
    cql_file_path.write_text(cql, encoding='utf-8')


# extract new entries from manually corrected texts + existing profile
@cli.command()
@click.argument("corrected-path", type=click.Path(exists=True))
@click.argument("dialect_path", type=click.Path(exists=True))
@click.option("-o", "--out-dir", type=click.Path(exists=True))
def profile_update(**kwargs):
    corrected = Path(kwargs["corrected_path"])
    dialect_path = Path(kwargs["dialect_path"])
    out_dir = Path(kwargs["out_dir"]) if kwargs["out_dir"] else None

    dump = ""
    for f in corrected.glob("*.txt"):
        dump += f.read_text(encoding="utf-8-sig") + "\n"

    rules = extract_new_entries(dump, dialect_path)
    if not out_dir:
        out = corrected.parent / (corrected.name + "_words.tsv")
    else:
        out = out_dir / (corrected.name + "_words.tsv")

    if not out.parent.is_dir():
        out.parent.mkdir(exist_ok=True)

    out.write_text(rules, encoding="utf-8-sig")


# FNR - Find and Replace with a list of regexes
@cli.command()
@click.argument("in-dir", type=click.Path(exists=True))
@click.argument("regex-file", type=click.Path(exists=True))
@click.option("-o", "--out-dir", type=click.Path(exists=True))
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
    # cli()
    save_config("test_path")
