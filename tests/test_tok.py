from click.testing import CliRunner

from pybo.cli import tok


def test_tok_dir():
    runner = CliRunner()
    runner.invoke(tok, ["tests/resources/shelving/", "--tags", "pl"])

def test_tok_file():
    runner = CliRunner()
    runner.invoke(tok, ["tests/resources/shelving/test_1.txt", "--tags", "p"])
