import pyqtgraph as pg


class graph_battery(pg.PlotItem):
    """Text plot item for displaying Battery Status."""

    def __init__(
        self,
        parent=None,
        name=None,
        labels=None,
        title="Battery Status",
        viewBox=None,
        axisItems=None,
        enableMenu=True,
        font=None,
        **kargs,
    ):
        super().__init__(parent, name, labels, title, viewBox, axisItems, enableMenu, **kargs)
        self.hideAxis("bottom")
        self.hideAxis("left")
        self.battery_text = pg.TextItem("100%", anchor=(0.5, 0.5), color="w")
        if font is not None:
            self.battery_text.setFont(font)
        self.addItem(self.battery_text)

    def update(self, value="100%"):
        self.battery_text.setText(str(value))