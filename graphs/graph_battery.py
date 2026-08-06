"""Battery graph module.

Displays the battery charge as a large centered text readout (percent). The
value comes from telemetry frame index 11 when present (the dummy-mode
simulator sends it; older hardware frames may not). If the frame has no
battery field the readout keeps its last value. Built on the shared
:class:`TextPlot` base so the readout never vanishes.
"""

import math

from graphs.base import TextPlot


class graph_battery(TextPlot):
    """Text plot item for displaying battery status."""

    def __init__(self, font=None, **kwargs):
        super().__init__(
            title="Battery Status", initial_text="100%", font=font, **kwargs
        )

    def update(self, value=None):
        """Refresh the readout with the latest battery percentage."""
        if value is None:
            return
        try:
            charge = float(value)
            if not math.isfinite(charge):
                return
            self.set_text(f"{charge:.0f}%")
        except (ValueError, TypeError):
            return
