"""
Shared pytest configuration for the CanSat Ground Station test suite.

Two things happen here:

* ``QT_QPA_PLATFORM=offscreen`` is forced before any Qt import so the GUI
  tests can run on machines with no display (CI, SSH, headless servers).
  The Qt plugin reads this environment variable when the ``QApplication`` is
  first constructed, so it must be set before pytest-qt builds the app.
* Coverage/plotting helpers are kept small on purpose; shared graph fixtures
  live in ``tests/conftest.py``.
"""

import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
