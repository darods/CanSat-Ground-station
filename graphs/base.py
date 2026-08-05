"""
Shared infrastructure for the live-scrolling telemetry plots.

This module provides two pieces of reusable machinery:

* ``ScrollingViewBox`` -- a pyqtgraph ``ViewBox`` that notices when the user
  grabs a plot with the mouse to pan or zoom. While the button is held down
  the live traces are frozen (so the data stops scrolling away from under the
  cursor) and, as soon as it is released, auto-ranging is re-enabled so the
  panel snaps straight back to the most recent telemetry.

* ``ScrollingPlot`` -- a :class:`pg.PlotItem` that renders one or more traces
  from a fixed-size numpy ring buffer. It takes care of shifting the buffer,
  refreshing the curves, downsampling and clip-to-view, so each concrete
  graph (altitude, pressure, temperature, ...) only has to push fresh values
  through :meth:`ScrollingPlot._push`.
"""

import numpy as np
import pyqtgraph as pg


class ScrollingViewBox(pg.ViewBox):
    """ViewBox that pauses live scrolling during a mouse drag and resumes after."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.live_paused = False

    def mouseDragEvent(self, ev, axis=None):
        # Freeze the plot while the user is panning/zooming...
        if ev.isStart():
            self.live_paused = True
        # ...and snap back to the live position as soon as they let go.
        elif ev.isFinish():
            self.live_paused = False
            self.enableAutoRange(axis=axis)
        super().mouseDragEvent(ev, axis)


class ScrollingPlot(pg.PlotItem):
    """Live plot that scrolls a fixed-size ring buffer of the latest samples.

    Parameters
    ----------
    title : str
        Plot title shown on the panel.
    pens : list[tuple[int, int, int]]
        One RGB pen colour per trace to display.
    names : list[str] | None
        Legend labels for the traces (only used when more than one pen).
    ylabel : str | None
        Text for the left (value) axis.
    buffer_size : int
        How many samples the ring buffer keeps (the visible window).
    viewBox : ScrollingViewBox | None
        Custom view box; a :class:`ScrollingViewBox` is created if omitted.
    hide_bottom : bool
        Hide the bottom (sample) axis (used by the multi-trace panels).
    """

    def __init__(
        self,
        title,
        pens,
        names=None,
        ylabel=None,
        buffer_size=300,
        viewBox=None,
        hide_bottom=False,
    ):
        super().__init__(title=title, viewBox=viewBox or ScrollingViewBox())
        if hide_bottom:
            self.hideAxis("bottom")
        if ylabel:
            self.setLabel("left", ylabel)

        self._buffer = np.zeros((buffer_size, len(pens)))
        self.ptr = 0
        self._curves = []

        if len(pens) > 1 and names:
            self.addLegend()
        for i, pen in enumerate(pens):
            curve = self.plot(pen=pen, name=names[i] if names else None)
            # Keep rendering fast even at high sample rates / large buffers.
            curve.setDownsampling(auto=True, method="peak")
            curve.setClipToView(True)
            self._curves.append(curve)

    @property
    def paused(self) -> bool:
        """True while the user is dragging the panel."""
        return self.vb.live_paused

    def _push(self, *values):
        """Append one telemetry sample to the ring buffer and refresh the trace.

        Called by the concrete graph classes from their ``update`` method.
        While the user is dragging the panel the sample is dropped so the
        trace stays frozen under the cursor; on release it jumps back to the
        current position automatically.
        """
        if self.paused:
            return
        self._buffer[:-1] = self._buffer[1:]
        self._buffer[-1] = values
        self.ptr += 1
        for i, curve in enumerate(self._curves):
            curve.setData(self._buffer[:, i])
            curve.setPos(self.ptr, 0)
