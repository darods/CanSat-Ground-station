"""Speed graph module.

Displays a scrolling trace of the scalar speed (m/s). The telemetry only
provides 3-axis acceleration (frame indices 8-10), so the velocity is
obtained by numerically integrating the acceleration in real time using the
wall clock between samples.
"""

import math
import time

from graphs.base import ScrollingPlot


class graph_speed(ScrollingPlot):
    """Live scrolling plot of the magnitude of the velocity (m/s)."""

    def __init__(self):
        super().__init__(title="Speed (m/s)", pens=[(29, 185, 84)], ylabel="m/s")
        self.vx = 0.0
        self.vy = 0.0
        self.vz = 0.0
        self.vzo = None  # baseline Z acceleration (gravity) removed before integrating
        self._last_t = time.monotonic()

    def update(self, ax, ay, az):
        """Integrate one acceleration sample and push the resulting speed."""
        try:
            ax, ay, az = float(ax), float(ay), float(az)
            # Reject nan/inf: once a non-finite value enters the integrator
            # it never recovers, so the speed trace would be dead forever.
            if not (math.isfinite(ax) and math.isfinite(ay) and math.isfinite(az)):
                return

            # Time step computed from the real wall clock so the integration
            # stays consistent no matter what the update interval is.
            now = time.monotonic()

            # While the user is dragging the panel the trace is frozen; freeze
            # the velocity too and just refresh the baseline so that resuming
            # the integration does not cause a sudden jump.
            if self.paused:
                self._last_t = now
                return

            dt = now - self._last_t
            self._last_t = now

            if self.vzo is None:
                self.vzo = az

            self.vx += ax * dt
            self.vy += ay * dt
            self.vz += (az - self.vzo) * dt  # gravity removed -> "dynamic" Z

            speed = math.sqrt(self.vx**2 + self.vy**2 + self.vz**2)
            self._push(speed)
        except (ValueError, TypeError):
            return
