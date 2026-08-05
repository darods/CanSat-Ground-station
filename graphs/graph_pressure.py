"""Barometric pressure graph module.

Displays a scrolling trace of the barometric pressure (hPa), read from
telemetry frame index 4, using the shared :class:`ScrollingPlot` base.
"""

from graphs.base import ScrollingPlot


class graph_pressure(ScrollingPlot):
    """Live scrolling plot of barometric pressure in hectopascals."""

    def __init__(self):
        super().__init__(
            title="Barometric Pressure (hPa)",
            pens=[(102, 252, 241)],
            ylabel="hPa",
        )

    def update(self, value):
        """Push the latest pressure sample onto the scrolling trace."""
        try:
            self._push(float(value))
        except (ValueError, TypeError):
            pass
