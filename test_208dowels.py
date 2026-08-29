"""
Pytest suite for the 208dowels Epitech-piscine exercise.

208dowels is a plain Python 3 script (no .py extension) that is meant to
run a chi-squared goodness-of-fit test on six observed class sizes
against a fitted binomial distribution. As documented in this project's
README, `compute_data()` is a stub: it ignores O1..O6 entirely and always
returns the same hard-coded placeholder table. These tests intentionally
capture and pin down that stub behaviour (see TestKnownStub below) rather
than trying to implement the missing statistics -- that's out of scope
for a QA pass.
"""
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).parent / "208dowels"
EXIT_SUCCESS = 0
EXIT_FAILURE = 84


def run(args):
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
    )


class TestHappyPath:
    def test_readme_example(self):
        result = run(["6", "4", "10", "18", "20", "19"])
        assert result.returncode == EXIT_SUCCESS
        out = result.stdout
        assert "x    | 1      | 2      | 3      | 4      | 5      | 6      | Total" in out
        assert "Ox    | 1      | 2      | 3      | 4      | 5      | 6      | 100" in out
        assert "Tx    | 1.0    | 2.0    | 3.0    | 4.0    | 5.0    | 6.0    | 100.0" in out
        assert "Distribution:             B(100, 1.0000)" in out
        assert "Chi-squared:              1.000" in out
        assert "Degrees of freedom:       1" in out
        assert "Fit validity:             1" in out

    def test_help_flag(self):
        result = run(["-h"])
        assert result.returncode == EXIT_SUCCESS
        assert "USAGE" in result.stderr
        assert "208dowels O1 O2 O3 O4 O5 O6" in result.stderr

    def test_long_help_flag(self):
        result = run(["--help"])
        assert result.returncode == EXIT_SUCCESS
        assert "USAGE" in result.stderr

    def test_negative_and_zero_observed_counts_are_accepted(self):
        # parse_argument only requires the 6 arguments to parse as int --
        # it does not validate that they are non-negative "counts". This
        # documents that (arguably permissive) real behaviour.
        result = run(["0", "-5", "10", "18", "20", "19"])
        assert result.returncode == EXIT_SUCCESS


class TestKnownStub:
    """compute_data() is a documented, pre-existing stub (see README's
    "Note on completeness"): it ignores O1..O6 and always returns the
    same fixed placeholder Ox/Tx rows. We pin this down explicitly so a
    future fix of compute_data() will make this test fail loudly and
    prompt someone to update it -- that's the point of documenting a
    known stub rather than silently tolerating it."""

    @pytest.mark.xfail(
        reason="compute_data() is a stub (see README): it always returns "
        "hardcoded Ox=1..6/Tx=1.0..6.0/Total=100 regardless of the real "
        "O1..O6 input, so distinct valid inputs currently produce "
        "identical output. This is expected to keep failing until the "
        "underlying statistics are actually implemented.",
        strict=True,
    )
    def test_different_inputs_should_give_different_output(self):
        a = run(["6", "4", "10", "18", "20", "19"])
        b = run(["4", "5", "13", "19", "20", "16"])
        assert a.returncode == EXIT_SUCCESS
        assert b.returncode == EXIT_SUCCESS
        assert a.stdout != b.stdout  # currently false: both are identical

    def test_stub_output_is_constant_regardless_of_input(self):
        """The mirror image of the xfail above, asserting what the
        program actually does today so a regression is caught."""
        a = run(["6", "4", "10", "18", "20", "19"])
        b = run(["4", "5", "13", "19", "20", "16"])
        assert a.returncode == EXIT_SUCCESS
        assert b.returncode == EXIT_SUCCESS
        assert a.stdout == b.stdout


class TestBadInput:
    def test_nine_arguments_from_legacy_test_sh_rejected(self):
        # test.sh in this repo passes 9 numbers (predates this version
        # of the exercise, per the README); confirm it's cleanly
        # rejected rather than silently mis-parsed.
        result = run(["6", "4", "10", "18", "20", "19", "11", "5", "7"])
        assert result.returncode == EXIT_FAILURE
        assert "USAGE" in result.stderr

    def test_too_few_arguments(self):
        result = run(["6", "4", "10"])
        assert result.returncode == EXIT_FAILURE
        assert "USAGE" in result.stderr

    def test_no_arguments(self):
        result = run([])
        assert result.returncode == EXIT_FAILURE
        assert "USAGE" in result.stderr

    def test_non_integer_argument_rejected(self):
        result = run(["6", "4", "10", "18", "20", "abc"])
        assert result.returncode == EXIT_FAILURE
        assert "USAGE" in result.stderr

    def test_float_argument_rejected(self):
        # int() rejects "18.5" outright (unlike float-tolerant scripts
        # in this collection).
        result = run(["6", "4", "10", "18.5", "20", "19"])
        assert result.returncode == EXIT_FAILURE
        assert "USAGE" in result.stderr


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
