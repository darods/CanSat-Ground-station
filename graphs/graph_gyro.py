"""Gyroscope graph module.

Displays scrolling traces of the pitch/roll/yaw rates (degrees per second),
read from telemetry frame indices 5-7, using the shared :class:`ScrollingPlot`
base.
"""

from graphs.base import ScrollingPlot


class graph_gyro(ScrollingPlot):
    """Live scrolling plot of the 3-axis gyroscope rates with a legend."""

    def __init__(self):
        super().__init__(
            title="Gyroscope (°/s)",
            pens=[(102, 252, 241), (29, 185, 84), (203, 45, 111)],
            names=["Pitch", "Roll", "Yaw"],
            hide_bottom=True,
        )

    def update(self, pitch, roll, yaw):
        """Push the latest gyroscope sample (pitch, roll, yaw) onto the traces."""
        try:
            self._push(float(pitch), float(roll), float(yaw))
        except (ValueError, TypeError):
            pass
