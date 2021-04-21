from click.testing import CliRunner

from pybo.cli import cli, profile_update


def test_tok():
    runner = CliRunner()
    runner.invoke(cli, ["tok", "tests/resources/shelving/", "--tags", "pl"])


def test_extract_rules():
    runner = CliRunner()
    runner.invoke(cli, ["extract-rules", "tests/resources/step2/step2"])

def test_extract_seg_rules():
    runner = CliRunner()
    runner.invoke(cli, ["extract-seg-rules", "tests/data/corpus1/corpus1_hd.txt", "--type", "hfr"])