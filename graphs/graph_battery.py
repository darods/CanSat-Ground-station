import pyqtgraph as pg

class graph_battery(pg.PlotItem):
    
    def __init__(self, parent=None, name=None, labels=None, title='Battery staus', viewBox=None, axisItems=None, enableMenu=True, font = None,**kargs):    
        super().__init__(parent, name, labels, title, viewBox, axisItems, enableMenu, **kargs)

        self.hideAxis('bottom')
        self.hideAxis('left')
        self.battery_text = pg.TextItem("test", anchor=(0.5, 0.5), color="w")
        if font != None:
            self.battery_text.setFont(font)
        self.addItem(self.battery_text)

    def update(self, value_chain):
        pass