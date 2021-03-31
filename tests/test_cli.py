from click.testing import CliRunner

from pybo.cli import cli, profile_update


def test_tok():
    runner = CliRunner()
    runner.invoke(cli, ["tok", "tests/resources/shelving/", "--tags", "pl"])


def test_extract_rules():
    runner = CliRunner()
    runner.invoke(cli, ["extract-rules", "tests/resources/step2/step2"])

def test_extract__seg_rules():
    runner = CliRunner()
    runner.invoke(cli, ["extract-seg-rules", "tests/corpus2/corpus2.txt", "--type", "hfr"])

def test_convert_cql2hfr():
    runner = CliRunner()
    runner.invoke(cli, ["convert-cql2hfr", "tests/resources/step2/cql_rules.txt"])

def test_convert_hfr2cql():
    runner = CliRunner()
    runner.invoke(cli, ["convert-hfr2cql", "tests/resources/step2/test_rules.txt"])