from click.testing import CliRunner

from pybo.cli import cli


def test_tok():
    runner = CliRunner()
    runner.invoke(cli, ["tok", "tests/resources/shelving/", "--tags", "pl"])


def test_extract_rules():
    runner = CliRunner()
    runner.invoke(cli, ["extract-rules", "tests/resources/step2/"])
