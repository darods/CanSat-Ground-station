"""Temperature graph module.

Displays a scrolling trace of the ambient temperature (Celsius), read from
telemetry frame index 3, using the shared :class:`ScrollingPlot` base.
"""

from contextlib import suppress

from graphs.base import ScrollingPlot


class graph_temperature(ScrollingPlot):
    """Live scrolling plot of temperature in degrees Celsius."""

    def __init__(self):
        super().__init__(title="Temperature (°C)", pens=[(29, 185, 84)], ylabel="°C")

    def update(self, value):
        """Push the latest temperature sample onto the scrolling trace."""
        with suppress(ValueError, TypeError):
            self._push(float(value))
