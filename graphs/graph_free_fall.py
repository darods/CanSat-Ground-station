"""Free-fall graph module.

Displays the free-fall detection flag as a large text readout (Yes/No),
read from telemetry frame index 2.
"""

import pyqtgraph as pg

# Values that count as "no free fall" in the telemetry frame.
_FALSE_VALUES = ("0", "False", "false", "")


class graph_free_fall(pg.PlotItem):
    """Text plot item for displaying the free-fall state."""

    def __init__(self, font=None, **kwargs):
        super().__init__(title="Free Fall", **kwargs)
        self.hideAxis("bottom")
        self.hideAxis("left")
        self.text = pg.TextItem("No", anchor=(0.5, 0.5), color="w")
        if font is not None:
            self.text.setFont(font)
        self.addItem(self.text)

    def update(self, value):
        """Refresh the readout with the latest free-fall flag."""
        self.text.setText("Yes" if str(value).strip() not in _FALSE_VALUES else "No")
