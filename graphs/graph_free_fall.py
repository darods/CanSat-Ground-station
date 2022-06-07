import pyqtgraph as pg

class graph_free_fall(pg.PlotItem):
    
    def __init__(self, parent=None, name=None, labels=None, title='Free fall', viewBox=None, axisItems=None, enableMenu=True, font = None,**kargs):    
        super().__init__(parent, name, labels, title, viewBox, axisItems, enableMenu, **kargs)

        self.hideAxis('bottom')
        self.hideAxis('left')
        self.text = pg.TextItem("test", anchor=(0.5, 0.5), color="w")
        if font != None:
            self.text.setFont(font)
        self.addItem(self.text)

    def update(self, value):
        self.text.setText('')
        if(value == '0'):
            self.text.setText('No')
        else:
            self.text.setText('Yes')