from typer.testing import CliRunner
from cluey.examples.ml import MLApp

runner = CliRunner()
cli = MLApp().main_app


def test_help_lists_only_commands_not_helper():
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    out = result.stdout
    # Commands exposed
    assert "train" in out
    assert "evaluate" in out
    # Helper method should not appear as a command
    assert "get-batches" not in out and "get_batches" not in out


def test_train_uses_items_and_batch_size_defaults_and_option():
    # With explicit batch size 2 and three items, expect 2 batches: [a,b], [c]
    result = runner.invoke(cli, ["train", "a", "b", "c", "--batch-size", "2"])
    assert result.exit_code == 0
    out = result.stdout
    assert "Training on 2 batches" in out
    assert "Training on batch: ['a', 'b']" in out
    assert "Training on batch: ['c']" in out


def test_evaluate_with_default_batch_size_two():
    # Default batch_size=2; four items → 2 batches
    result = runner.invoke(cli, ["evaluate", "w", "x", "y", "z"])
    assert result.exit_code == 0
    out = result.stdout
    assert "Evaluating 2 batches:" in out
    assert "Evaluating on batch: ['w', 'x']" in out
    assert "Evaluating on batch: ['y', 'z']" in out


def test_subcommand_help_includes_merged_options_from_helper():
    # Because @cluey.main("get_batches") merges helper params,
    # both commands should show --items and --batch-size in their help.
    train_help = runner.invoke(cli, ["train", "--help"])
    assert train_help.exit_code == 0
    th = train_help.stdout
    assert "--batch-size" in th
    # items is a positional ARG (list[str]); help text may show as ARG
    assert "ITEMS" in th or "items" in th

    eval_help = runner.invoke(cli, ["evaluate", "--help"])
    assert eval_help.exit_code == 0
    eh = eval_help.stdout
    assert "--batch-size" in eh
    assert "ITEMS" in eh or "items" in eh
