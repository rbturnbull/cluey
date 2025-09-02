from cluey.testing import CliRunner
from cluey.examples.productionml import ProductionMLApp

runner = CliRunner()
app = ProductionMLApp()
main_cli = app.main_app
tools_cli = app.tools_app


def test_main_cli_only_predict_visible():
    r = runner.invoke(main_cli, ["--help"])
    assert r.exit_code == 0
    out = r.stdout
    assert "List of items to process" in out
    assert "Predict using model in batches" in out
    assert "predict    Predict using model in batches" not in out
    assert "train " not in out
    assert "evaluate " not in out
    assert "cite " not in out


def test_predict_runs_with_items_and_batch_size():
    r = runner.invoke(main_cli, ["A", "B", "C", "D", "--batch-size", "3"])
    assert r.exit_code == 0
    out = r.stdout
    assert "Predicting over 2 batches:" in out
    assert "Predicting on batch: ['A', 'B', 'C']" in out
    assert "Predicting on batch: ['D']" in out


def test_tools_cli_lists_train_evaluate_cite():
    r = runner.invoke(tools_cli, ["--help"])
    assert r.exit_code == 0
    out = r.stdout
    for cmd in ("train", "evaluate", "cite"):
        assert cmd in out
    assert "Commands" in out
    assert "cite       Cite this model." in out
    assert "evaluate   Evaluate the model." in out
    assert "predict    Predict using model in batches" in out
    assert "train      Train the model." in out


def test_tools_train_and_evaluate_delegate_and_accept_options():
    r1 = runner.invoke(tools_cli, ["train", "a", "b", "c", "--batch-size", "2"])
    assert r1.exit_code == 0
    assert "Training on 2 batches" in r1.stdout

    r2 = runner.invoke(tools_cli, ["evaluate", "w", "x", "y", "z"])
    assert r2.exit_code == 0
    assert "Evaluating 2 batches:" in r2.stdout


def test_tools_cite_prints_citation():
    r = runner.invoke(tools_cli, ["cite"])
    assert r.exit_code == 0
    assert "Please cite the paper" in r.stdout
