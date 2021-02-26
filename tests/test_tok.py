from click.testing import CliRunner

from pybo.cli import tok


def test_tok():
    runner = CliRunner()
    runner.invoke(tok, ["tests/resources/shelving/", "", ""])
