from cluey.testing import CliRunner
from cluey.examples.stringtools import StringTools

runner = CliRunner()
app = StringTools()
cli = app.main_app  # Typer app behind .main()



def test_lowercase_basic():
    result = runner.invoke(cli, ["lowercase", "Hello"])
    assert result.exit_code == 0
    # Should print the lowercase version and return it
    assert "hello" in result.stdout


def test_clean_defaults_no_changes():
    # Accents and non-ascii removal are False by default
    result = runner.invoke(cli, ["clean", "Café"])
    assert result.exit_code == 0
    assert "Café" in result.stdout


def test_clean_strip_accents_and_ascii():
    # Strip accents and remove non-ascii; emoji should disappear, é -> e
    result = runner.invoke(
        cli,
        ["clean", "Café ☕️", "--strip-accents", "--ascii"],
    )
    assert result.exit_code == 0
    out = result.stdout
    assert "Cafe" in out
    # Sanity check: coffee emoji should be gone
    assert "☕" not in out


def test_count_vowels_inherits_options_and_works():
    # count-vowels should expose --strip-accents/--ascii via 'clean'
    result_help = runner.invoke(cli, ["count-vowels", "--help"])
    assert result_help.exit_code == 0
    help_text = result_help.stdout
    assert "--strip-accents" in help_text
    assert "--ascii" in help_text

    # Now run with an accented string; with strip-accents, expect 2 vowels (a,e)
    result = runner.invoke(cli, ["count-vowels", "Café ☕️", "--strip-accents"])
    assert result.exit_code == 0
    assert "Vowels: 2" in result.stdout
