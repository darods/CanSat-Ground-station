"""Altitude graph module.

Displays a scrolling trace of the CanSat relative altitude (m), read from
telemetry frame index 1, using the shared :class:`ScrollingPlot` base.
"""

from graphs.base import ScrollingPlot


class graph_altitude(ScrollingPlot):
    """Live scrolling plot of altitude in meters."""

    def __init__(self):
        super().__init__(title="Altitude (m)", pens=[(29, 185, 84)], ylabel="m")

    def update(self, value):
        """Push the latest altitude sample onto the scrolling trace."""
        try:
            self._push(float(value))
        except (ValueError, TypeError):
            pass
