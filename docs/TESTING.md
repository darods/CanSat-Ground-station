# Testing

This project is a development tool that will keep changing, so every change
to the telemetry pipeline should be covered by a unit test. This guide
explains how the tests are organised, how to run them, and how to add a new
one.

## Running the tests

Run the whole suite:

```sh
uv run pytest
```

Run a single file or a selection:

```sh
uv run pytest tests/test_communication.py
uv run pytest -k "battery or free_fall"
```

Show the coverage report instead of the terminal summary:

```sh
uv run pytest --cov-report=html
```

All commands work from the project root. Every run produces a coverage
report for `communication`, `dataBase`, `graphs` and `main`; the summary
prints the lines that are still uncovered so you know what to test next.

## CI

The same checks run on GitHub Actions for every push/PR (`.github/workflows/ci.yml`):
`ruff check` + `ruff format --check`, the test suite on Ubuntu/macOS/Windows,
an import smoke check, `pip-audit` for dependency vulnerabilities and
`bandit -c pyproject.toml` for source scanning. Lint and formatting are
enforced there, so run them locally before pushing:

```sh
uv run ruff check .
uv run ruff format .
uv run pip-audit
uv run bandit -c pyproject.toml -r communication.py dataBase.py main.py graphs/
```

## Headless mode

All tests run **headless** (`QT_QPA_PLATFORM=offscreen`), which is forced in
the root `conftest.py` before any Qt import. You never need a display, and
the same command works on a CI machine. Graph panels are created but never
shown, so there are no windows flashing during the run.

## Test layout

```
conftest.py            # headless setup (QT_QPA_PLATFORM=offscreen)
tests/
  conftest.py          # shared fixtures: one per graph panel
  test_communication.py# dummy flight simulator + frame validation
  test_dataBase.py     # CSV logging
  test_graphs.py       # ScrollingPlot / TextPlot behaviour
  test_dispatch.py     # main.dispatch_frame frame -> panels mapping
```

Each test module mirrors one source module, and each file starts with a
docstring explaining *why* those tests exist (the contract they pin down).

## Fixtures

`pytest-qt` provides the `qtbot` fixture, which guarantees a `QApplication`
exists. `tests/conftest.py` adds one fixture per graph panel
(`altitude_graph`, `time_graph`, ...) so a graph test reads:

```python
def test_push_advances_pointer(qtbot, altitude_graph):
    altitude_graph.update("10")
    altitude_graph.update("20")
    assert altitude_graph.ptr == 2
```

## Conventions

1. **Prefer `tmp_path` over real files.** Tests that touch `DataBase`
   always use the `tmp_path` fixture so nothing is written into the repo.
2. **Never assert exact wall-clock or timestamps.** The dummy mission clock
   is real-time and `DataBase.guardar` appends a `time.strftime` timestamp.
   Only assert relationships (monotonic, increasing, roughly equal) and
   indices, not concrete values.
3. **Sample the simulator at an arbitrary time** with the `frame_at`
   helper in `tests/test_communication.py` — it fast-forwards the internal
   monotonic clock, keeping the physics tests deterministic.
4. **Markers must be registered.** Pytest runs with `--strict-markers`.
   If you add a marker, register it under `[tool.pytest.ini_options].markers`
   in `pyproject.toml`.
5. **No GUI entry points in coverage.** `main()` and the
   `if __name__ == "__main__"` block are marked `# pragma: no cover`; test
   the extracted `dispatch_frame` instead of launching the app.
6. **Test the contract, not the internals.** If you change the telemetry
   schema (README documents it), update `tests/test_dispatch.py` too.

## Adding a test

1. Find the source module you changed: `communication.py`, `dataBase.py`,
   `graphs/base.py`, `main.py` (only `dispatch_frame` is tested).
2. Open the matching test file in `tests/`.
3. Add a test that exercises the new behaviour. Use the fixtures above
   rather than constructing graphs inline.
4. Run it: `uv run pytest tests/test_<module>.py`.
5. Run the full suite to make sure nothing else broke, then check the
   coverage summary to confirm the new code is covered.
