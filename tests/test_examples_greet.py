from cluey.testing import CliRunner
from cluey.examples.greet import GreetApp

runner = CliRunner()
app = GreetApp()
cli = app.main_app


def test_greet_name():
    result = runner.invoke(cli, "Alice")
    assert result.exit_code == 0
    assert "Hello, Alice!" in result.stdout


def test_greet_help():
    result = runner.invoke(cli, "greet --help")
    assert result.exit_code == 0
    assert "name" in result.stdout
    assert "Show the version of this CLI" in result.stdout


def test_version_flag():
    result = runner.invoke(cli, "--version")
    assert result.exit_code == 0
    assert "GreetApp version" in result.stdout


def test_version_flag_shortcut():
    result = runner.invoke(cli, "-v")
    assert result.exit_code == 0
    assert "GreetApp version" in result.stdout


def test_test_greet_name_programatic(capsys):
    app.greet("Alice")
    out, err = capsys.readouterr()
    assert err == ""
    assert out.startswith("Hello, Alice!")


def test_version_programatic():
    version = app.version()
    assert version.startswith("GreetApp version")
