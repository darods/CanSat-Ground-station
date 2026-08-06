"""Elapsed-time graph module.

Displays the mission elapsed time as a large centered text readout (minutes),
converted from the millisecond timestamp in telemetry frame index 0. Built on
the shared :class:`TextPlot` base so the readout never vanishes.
"""

import math

from graphs.base import TextPlot


class graph_time(TextPlot):
    """Text plot item for displaying elapsed time in minutes."""

    def __init__(self, font=None, **kwargs):
        super().__init__(title="Time (min)", initial_text="0.0", font=font, **kwargs)

    def update(self, value):
        """Refresh the readout with the latest elapsed-time sample (ms)."""
        try:
            minutes = float(value) / 60000.0
            if not math.isfinite(minutes):
                return
            self.set_text(f"{minutes:.2f}")
        except (ValueError, TypeError):
            return
