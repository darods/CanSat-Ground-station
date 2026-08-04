import pyqtgraph as pg


class graph_time(pg.PlotItem):
    """Text plot item for displaying Elapsed Time (min)."""

    def __init__(
        self,
        parent=None,
        name=None,
        labels=None,
        title="Time (min)",
        viewBox=None,
        axisItems=None,
        enableMenu=True,
        font=None,
        **kargs,
    ):
        super().__init__(parent, name, labels, title, viewBox, axisItems, enableMenu, **kargs)
        self.hideAxis("bottom")
        self.hideAxis("left")
        self.time_text = pg.TextItem("0.0", anchor=(0.5, 0.5), color="w")
        if font is not None:
            self.time_text.setFont(font)
        self.addItem(self.time_text)

    def update(self, value):
        try:
            val_num = float(value)
            tiempo = round(val_num / 60000.0, 2)
            self.time_text.setText(str(tiempo))
        except (ValueError, TypeError):
            pass