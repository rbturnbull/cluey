from cluey.testing import CliRunner
from cluey.examples.arithmetic import ArithmeticApp

runner = CliRunner()
cli = ArithmeticApp().main_app


def test_add_default():
    result = runner.invoke(cli, ["add", "3", "2"])
    assert result.exit_code == 0
    assert "5" in result.stdout


def test_subtract_default():
    result = runner.invoke(cli, ["subtract", "3", "2"])
    assert result.exit_code == 0
    assert "1" in result.stdout
