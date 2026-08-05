"""Elapsed-time graph module.

Displays the mission elapsed time as a large text readout (minutes),
converted from the millisecond timestamp in telemetry frame index 0.
"""

import pyqtgraph as pg


class graph_time(pg.PlotItem):
    """Text plot item for displaying elapsed time in minutes."""

    def __init__(self, font=None, **kwargs):
        super().__init__(title="Time (min)", **kwargs)
        self.hideAxis("bottom")
        self.hideAxis("left")
        self.time_text = pg.TextItem("0.0", anchor=(0.5, 0.5), color="w")
        if font is not None:
            self.time_text.setFont(font)
        self.addItem(self.time_text)

    def update(self, value):
        """Refresh the readout with the latest elapsed-time sample (ms)."""
        try:
            minutes = float(value) / 60000.0
            self.time_text.setText(f"{minutes:.2f}")
        except (ValueError, TypeError):
            pass
