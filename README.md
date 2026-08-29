# 208dowels

An Epitech "piscine" statistics exercise about goodness-of-fit testing. Given
six observed class sizes `O1..O6` (e.g. counts of manufactured dowels that
fall into six size/length classes), the intended behaviour is to compare the
observed distribution against a theoretical binomial distribution `B(100, p)`
and report a chi-squared statistic, degrees of freedom, and whether the fit
is statistically valid. Like the other exercises here it's implemented in
Python 3 rather than C — `208dowels` has no `.py` extension but starts with
`#!/usr/bin/env python3`.

**Note on completeness:** `compute_data()` in the current source ignores the
`O1..O6` values it's given and always returns the same hard-coded
placeholder numbers (classes 1–6, `Ox` = 1..6, `Tx` = 1.0..6.0, `Total` =
100). So the table/chi-squared/degrees-of-freedom/fit-validity values printed
below are constant regardless of input — the statistical computation itself
was never finished. The example output is reproduced accurately from the
actual code, not fabricated.

## Build

No Makefile, no compilation. `208dowels` is a Python 3 script.

**Windows note:** run it with the Python launcher:

```
python 208dowels [args...]
```

## Usage

```
python 208dowels -h
```

```
USAGE
        208dowels O1 O2 O3 O4 O5 O6

DESCRIPTION
        Oi      size of the observed class
```

Exactly six integer arguments are required (the bundled `test.sh` in this
repo actually passes nine numbers, e.g. `6 4 10 18 20 19 11 5 7`, which this
implementation rejects with the usage/error message and exit code 84 — that
script predates/mismatches this version of the exercise).

A valid invocation:

```
python 208dowels 6 4 10 18 20 19
```

```
   x    | 1      | 2      | 3      | 4      | 5      | 6      | Total
  Ox    | 1      | 2      | 3      | 4      | 5      | 6      | 100
  Tx    | 1.0    | 2.0    | 3.0    | 4.0    | 5.0    | 6.0    | 100.0
Distribution:             B(100, 1.0000)
Chi-squared:              1.000
Degrees of freedom:       1
Fit validity:             1
```

## How it works

- `parse_argument` requires exactly 7 argv entries (program name + 6
  integers `O1..O6`); anything else, or `-h`/`--help`, prints the usage
  block (exit 0 for help, exit 84 for bad arguments).
- `compute_data` is meant to turn `O1..O6` into the observed frequency row
  (`Ox`) and the theoretical/expected frequency row (`Tx`) under a fitted
  binomial model, but currently returns fixed placeholder rows regardless
  of the input.
- `show_array` prints the `x` / `Ox` / `Tx` table with fixed-width columns;
  `show_distribution`, `show_chi_squared`, `show_degrees_of_freedom` and
  `show_fit_validity` print the remaining summary lines. All of these are
  fed the same placeholder value (`1`) from `main`, so the "statistics"
  section is currently a stub as well.
