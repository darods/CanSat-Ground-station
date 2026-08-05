"""
Unit tests for the CSV data logger (``dataBase.py``).

The logger appends one row per telemetry frame (the frame fields plus a local
timestamp) only while recording is enabled. Tests use ``tmp_path`` so they
never write into the repository.
"""

import csv

from dataBase import DataBase


def test_guardar_writes_row(tmp_path):
    db = DataBase(filename=tmp_path / "flight.csv")
    db.start()
    db.guardar(["0", "100", "1", "20.1", "1013", "0", "0", "0", "0", "0", "9.8"])

    rows = list(csv.reader((tmp_path / "flight.csv").open()))
    assert len(rows) == 1
    assert rows[0][:11] == [
        "0",
        "100",
        "1",
        "20.1",
        "1013",
        "0",
        "0",
        "0",
        "0",
        "0",
        "9.8",
    ]
    # A local timestamp column is appended.
    assert len(rows[0]) == 12


def test_guardar_appends_multiple_rows(tmp_path):
    db = DataBase(filename=tmp_path / "flight.csv")
    db.start()
    db.guardar(["a"])
    db.guardar(["b"])

    rows = list(csv.reader((tmp_path / "flight.csv").open()))
    assert len(rows) == 2


def test_guardar_does_nothing_while_stopped(tmp_path):
    db = DataBase(filename=tmp_path / "flight.csv")
    db.guardar(["0", "100"])
    assert not (tmp_path / "flight.csv").exists()


def test_start_and_stop_toggle_recording(tmp_path):
    db = DataBase(filename=tmp_path / "flight.csv")
    assert db.state is False
    db.start()
    assert db.state is True
    db.stop()
    assert db.state is False


def test_guardar_ignores_empty_data(tmp_path):
    db = DataBase(filename=tmp_path / "flight.csv")
    db.start()
    db.guardar([])  # must not crash and must not write an empty line
    assert not (tmp_path / "flight.csv").exists()


def test_guardar_neutralizes_formula_injection(tmp_path):
    # Spreadsheets execute cells starting with =, + or @ as formulas; the
    # logger must neutralise them so a malicious frame can't run code on open.
    db = DataBase(filename=tmp_path / "flight.csv")
    db.start()
    db.guardar(["=2+5", "+SUM(A1)", "@cmd", "  =1+1", "normal"])
    rows = list(csv.reader((tmp_path / "flight.csv").open()))
    assert rows[0][0].startswith("'=")
    assert rows[0][1].startswith("'+")
    assert rows[0][2].startswith("'@")
    assert rows[0][3].startswith("'=")
    assert rows[0][4] == "normal"


def test_guardar_keeps_negative_numbers(tmp_path):
    # "-" is a legitimate numeric prefix and must not be neutralised.
    db = DataBase(filename=tmp_path / "flight.csv")
    db.start()
    db.guardar(["-5.5"])
    rows = list(csv.reader((tmp_path / "flight.csv").open()))
    assert rows[0][0] == "-5.5"


def test_backwards_compatible_alias():
    assert DataBase is not None
