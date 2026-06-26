# Copilot Instructions for This Repository

## Project Context

This repository is a take-home assessment for a romance novel data pipeline. The core goal is to implement the transform and analysis stages clearly and correctly.

Primary scripts:
- `process_raw_data.py` (required)
- `analyse_processed_data.py` (required)

Optional scripts/tasks:
- `get_keywords.py` (optional)
- architecture diagram for future pipeline (optional)
- Tableau Public dashboard link (optional)

## Required Behavior: `process_raw_data.py`

Treat this script as a command-line program that takes exactly one argument: the path to a raw `.csv` input file.

When implementing or modifying this script:
- Read input files in the same format as `RAW_DATA_0.csv`, `RAW_DATA_1.csv`, and `RAW_DATA_4.csv`.
- Write a single output file named `PROCESSED_DATA.csv`.
- Always overwrite any existing `PROCESSED_DATA.csv`.
- Output columns must be exactly:
  - `title`
  - `author_name`
  - `year`
  - `rating`
  - `ratings`
- Ensure `title` and `author_name` are text fields.
- Ensure `year`, `rating`, and `ratings` are numeric fields.
- Clean titles by removing bracketed information (for example, series/format text in `(...)` or `[...]`).
- Exclude rows with missing title or missing author.
- Sort final output by descending `rating`.
- Keep behavior aligned with `EXAMPLE_DATA_4.csv` for `RAW_DATA_4.csv`.

## Required Behavior: `analyse_processed_data.py`

Treat this script as a program that reads `PROCESSED_DATA.csv` and generates two image outputs:
- `decade_releases.png`: pie chart of release proportions by decade.
- `top_authors.png`: sorted bar chart of total ratings for the ten most-rated authors.

When implementing visualizations:
- Aggregate decades from the `year` field.
- Aggregate author totals from the `ratings` field.
- Ensure charts are readable and deterministically generated from processed data.

## Coding and Design Expectations

- Prioritize correctness first, then code quality and clarity.
- Keep data transformations explicit and easy to review.
- Validate assumptions about input columns and handle malformed data gracefully.
- Use clear function boundaries for loading, cleaning, transforming, and writing data.
- Keep scripts runnable from CLI without hidden dependencies.
- Do not introduce unrelated framework or infrastructure complexity.

## Output and File Discipline

- Do not change required output filenames.
- Do not append to processed outputs; overwrite them.
- Keep generated artifacts limited to the files specified by each task unless explicitly requested otherwise.

## Optional Scope Guidance

If optional work is requested:
- `get_keywords.py` should produce `top_keywords.png` with the top 20 keywords from titles.
- Architecture work should reflect: object storage ingestion, central database accumulation, and an analytics dashboard.
- Tableau work should include a shareable public link.

## Assessment Mindset

There are no automated tests in this project. Favor robust, readable, well-structured code and include lightweight validation where useful.