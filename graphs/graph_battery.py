"""Battery graph module.

Displays the battery charge as a large text readout (percent). The value
comes from telemetry frame index 11 when present (the dummy-mode simulator
sends it; older hardware frames may not). If the frame has no battery field
the readout keeps its last value.
"""

import pyqtgraph as pg


class graph_battery(pg.PlotItem):
    """Text plot item for displaying battery status."""

    def __init__(self, font=None, **kwargs):
        super().__init__(title="Battery Status", **kwargs)
        self.hideAxis("bottom")
        self.hideAxis("left")
        self.battery_text = pg.TextItem("100%", anchor=(0.5, 0.5), color="w")
        if font is not None:
            self.battery_text.setFont(font)
        self.addItem(self.battery_text)

    def update(self, value=None):
        """Refresh the readout with the latest battery percentage."""
        if value is None:
            return
        try:
            self.battery_text.setText(f"{float(value):.0f}%")
        except (ValueError, TypeError):
            pass
