from cluey.testing import CliRunner
from cluey.examples.extendedml import ExtendedMLApp

runner = CliRunner()
cli = ExtendedMLApp().main_app



def test_help_lists_commands_and_hides_helper():
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    out = result.stdout
    # Inherited commands + new one
    assert "train" in out
    assert "evaluate" in out
    assert "stats" in out
    # Helper method must not be exposed
    assert "get-batches" not in out and "get_batches" not in out


def test_train_uses_overridden_get_batches_with_lowercase():
    # With --lowercase, items should appear lowercased in train output
    result = runner.invoke(
        cli, ["train", "A", "B", "C", "--batch-size", "2", "--lowercase"]
    )
    assert result.exit_code == 0
    out = result.stdout
    # two batches: ['a','b'] and ['c']
    assert "Training on 2 batches" in out
    assert "Training on batch: ['a', 'b']" in out
    assert "Training on batch: ['c']" in out
    # ensure uppercase versions are not present
    assert "['A', 'B']" not in out
    assert "['C']" not in out


def test_evaluate_respects_parent_defaults_and_overrides():
    # Default batch_size=2, items lowercase applied
    result = runner.invoke(
        cli, ["evaluate", "X", "y", "Z", "--lowercase"]
    )
    assert result.exit_code == 0
    out = result.stdout
    assert "Evaluating 2 batches:" in out
    assert "Evaluating on batch: ['x', 'y']" in out or "Evaluating on batch: ['x', 'y']" in out
    assert "Evaluating on batch: ['z']" in out
    # uppercase should not remain
    assert "['X', 'y']" not in out
    assert "['Z']" not in out


def test_stats_outputs_sizes_and_total_and_has_merged_options_in_help():
    # Help should include merged options/args from get_batches, including --lowercase and --batch-size
    help_result = runner.invoke(cli, ["stats", "--help"])
    assert help_result.exit_code == 0
    ht = help_result.stdout
    assert "--batch-size" in ht
    assert "--lowercase" in ht
    # items is a positional list arg; presence varies by formatter, check for a placeholder
    assert "ITEMS" in ht or "items" in ht

    # Now run stats with explicit items and batch size
    run_result = runner.invoke(
        cli, ["stats", "a", "b", "c", "d", "e", "--batch-size", "2"]
    )
    assert run_result.exit_code == 0
    out = run_result.stdout
    assert "3 batches" in out
    assert "sizes=[2, 2, 1]" in out
    assert "total_items=5" in out
