from typer.testing import CliRunner
from cluey.examples.greet import GreetApp

runner = CliRunner()
cli = GreetApp().main_app


def test_greet_default():
    result = runner.invoke(cli, ["Alice"])
    assert result.exit_code == 0
    assert "Hello, Alice!" in result.stdout


def test_greet_help():
    result = runner.invoke(cli, ["greet", "--help"])
    assert result.exit_code == 0
    assert "name" in result.stdout
    assert "Show the version of this CLI" in result.stdout


def test_version_flag():
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert "GreetApp version" in result.stdout
