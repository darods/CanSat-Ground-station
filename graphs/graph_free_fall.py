import pyqtgraph as pg


class graph_free_fall(pg.PlotItem):
    """Text plot item for displaying Free Fall state."""

    def __init__(
        self,
        parent=None,
        name=None,
        labels=None,
        title="Free Fall",
        viewBox=None,
        axisItems=None,
        enableMenu=True,
        font=None,
        **kargs,
    ):
        super().__init__(parent, name, labels, title, viewBox, axisItems, enableMenu, **kargs)
        self.hideAxis("bottom")
        self.hideAxis("left")
        self.text = pg.TextItem("No", anchor=(0.5, 0.5), color="w")
        if font is not None:
            self.text.setFont(font)
        self.addItem(self.text)

    def update(self, value):
        val_str = str(value).strip()
        if val_str in ("0", "False", "false", ""):
            self.text.setText("No")
        else:
            self.text.setText("Yes")