"""3-axis acceleration graph module.

Displays scrolling traces of the X/Y/Z acceleration (m/s²), read from
telemetry frame indices 8-10, using the shared :class:`ScrollingPlot` base.
"""

from contextlib import suppress

from graphs.base import ScrollingPlot


class graph_acceleration(ScrollingPlot):
    """Live scrolling plot of the 3-axis acceleration with a legend."""

    def __init__(self):
        super().__init__(
            title="Acceleration (m/s²)",
            pens=[(102, 252, 241), (29, 185, 84), (203, 45, 111)],
            names=["X", "Y", "Z"],
            hide_bottom=True,
        )

    def update(self, ax, ay, az):
        """Push the latest acceleration sample (X, Y, Z) onto the traces."""
        with suppress(ValueError, TypeError):
            self._push(float(ax), float(ay), float(az))
