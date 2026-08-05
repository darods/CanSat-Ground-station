"""Free-fall graph module.

Displays the free-fall detection flag as a large centered text readout
(Yes/No), read from telemetry frame index 2. Built on the shared
:class:`TextPlot` base so the readout never vanishes.
"""

from graphs.base import TextPlot

# Values that count as "no free fall" in the telemetry frame.
_FALSE_VALUES = ("0", "False", "false", "")


class graph_free_fall(TextPlot):
    """Text plot item for displaying the free-fall state."""

    def __init__(self, font=None, **kwargs):
        super().__init__(title="Free Fall", initial_text="No", font=font, **kwargs)

    def update(self, value):
        """Refresh the readout with the latest free-fall flag."""
        self.set_text("Yes" if str(value).strip() not in _FALSE_VALUES else "No")
