import sys
from unittest.mock import Mock

import click
from click.testing import CliRunner
import pytest
import typer

from cluey.cli import Cluey, ClueyTyper, flag, method


@pytest.mark.parametrize("hook", [sys.__excepthook__, typer.main.except_hook])
def test_cluey_typer_call_forwards_arguments_and_returns_result(monkeypatch, hook):
    monkeypatch.setattr(sys, "excepthook", hook)
    app = ClueyTyper(Cluey())
    result = object()
    command = Mock(return_value=result)
    getcommand = Mock(return_value=command)
    monkeypatch.setattr(app, "getcommand", getcommand)

    assert app(["example"], standalone_mode=False, prog_name="cluey") is result

    getcommand.assert_called_once_with()
    command.assert_called_once_with(["example"], standalone_mode=False, prog_name="cluey")
    assert sys.excepthook is typer.main.except_hook


@pytest.mark.parametrize("failure_stage", ["getcommand", "command"])
@pytest.mark.parametrize("enabled,show_locals,short", [(True, False, True), (False, True, False)])
def test_cluey_typer_call_attaches_config_and_reraises(monkeypatch, failure_stage, enabled, show_locals, short):
    monkeypatch.setattr(sys, "excepthook", sys.__excepthook__)
    app = ClueyTyper(
        Cluey(),
        pretty_exceptions_enable=enabled,
        pretty_exceptions_show_locals=show_locals,
        pretty_exceptions_short=short,
    )
    error = ValueError("command failed")
    command = Mock(side_effect=error)
    getcommand = Mock(return_value=command)
    if failure_stage == "getcommand":
        getcommand.side_effect = error
    monkeypatch.setattr(app, "getcommand", getcommand)

    with pytest.raises(ValueError, match="command failed") as exc_info:
        app()

    assert exc_info.value is error
    config = getattr(error, typer.main._typer_developer_exception_attr_name)
    assert isinstance(config, typer.main.DeveloperExceptionConfig)
    assert config.pretty_exceptions_enable is enabled
    assert config.pretty_exceptions_show_locals is show_locals
    assert config.pretty_exceptions_short is short
    assert sys.excepthook is typer.main.except_hook


@pytest.mark.parametrize("entry_point,app_name,other_app_name", [
    ("main", "main_app", "tools_app"),
    ("tools", "tools_app", "main_app"),
])
def test_class_entry_point_invokes_correct_app(entry_point, app_name, other_app_name):
    instances = []

    class EntryPointCluey(Cluey):
        def __init__(self):
            self.main_app = Mock()
            self.tools_app = Mock()
            instances.append(self)

    getattr(EntryPointCluey, entry_point)()

    assert len(instances) == 1
    instance = instances[0]
    getattr(instance, app_name).assert_called_once_with()
    getattr(instance, other_app_name).assert_not_called()


@pytest.mark.parametrize("kwargs,expected", [({}, 42), ({"value": 0}, 0)])
def test_get_kwargs_uses_option_default_when_omitted(kwargs, expected):
    class OptionCluey(Cluey):
        @method
        def option_value(self, value: int = typer.Option(42)):
            return value

    app = OptionCluey()

    assert app.option_value.get_kwargs(kwargs) == {"value": expected}
    assert app.original_kwargs["option_value"] == kwargs
    assert app.option_value(**kwargs) == expected


@pytest.mark.parametrize("shortcut", ["v", "-v"])
def test_patch_command_normalizes_flag_shortcut(shortcut):
    class FlagCluey(Cluey):
        @flag(shortcut=shortcut)
        def version(self):
            return "Version 1.0"

    app = FlagCluey()
    command = click.Command("example")
    app.main_app.patch_command(command)

    assert command.params[0].opts == ["--version", "-v"]
    result = CliRunner().invoke(command, ["-v"])
    assert result.exit_code == 0
    assert "Version 1.0" in result.output


def test_modify_signature_prints_signature_error(capsys):
    app = Cluey()

    @method
    def dependency(self, value: int = 1):
        return value

    @method("dependency")
    def command(self, *, verbose: bool = False):
        return verbose

    app.dependency = dependency

    # Merging these parameters puts a positional parameter after a keyword-only one.
    app.modify_signature(command)

    captured = capsys.readouterr()
    assert "ERROR in Method(" in captured.out
    assert "command" in captured.out
    assert "wrong parameter order: keyword-only parameter before positional or keyword parameter" in captured.out
    assert captured.err == ""
    assert command.signature_ready is True
    assert "__signature__" not in command.func.__dict__


class BaseCluey(Cluey):
    @method
    def add_one(self, value:int) -> int:
        raise NotImplementedError


class ChildCluey(BaseCluey):
    @method
    def add_one(self, value:int):
        return value + 1


def test_multiple_instances():
    # Check that a base app can raise a not implemented error
        
    app = BaseCluey()
    with pytest.raises(NotImplementedError):
        app.add_one(42)

    # Check if new app can override the function

    child_app = ChildCluey()
    assert child_app.add_one(42) == 43

    # Check that the first app still raises not implemented
    with pytest.raises(NotImplementedError):
        app.add_one(42)

    # Check that new definition of child hasn't affected parent class
    new_base_app = BaseCluey()
    with pytest.raises(NotImplementedError):
        new_base_app.add_one(42)
