

from qtpy import QtCore, QtWidgets


class FlowLayout(QtWidgets.QLayout):
    def __init__(self, parent=None, margin=0, spacing=0):
        super(FlowLayout, self).__init__(parent)
 
        if parent is not None:
            self.setMargin(margin)
 
        self.setSpacing(spacing)
 
        self.itemList = []
 
    def __del__(self):
        self.clear()

    def clear(self):
        item = self.takeAt(0)
        while item:
            w = item.widget()
            if w:
                w.deleteLater()
            item = self.takeAt(0)

    def addItem(self, item):
        self.itemList.append(item)
 
    def count(self):
        return len(self.itemList)
 
    def itemAt(self, index):
        if index >= len(self.itemList):
            return None

        if index >= 0:
            return self.itemList[index]

        return None
 
    def takeAt(self, index):
        if index >= 0 and index < len(self.itemList):
            return self.itemList.pop(index)
 
        return None
 
    def expandingDirections(self):
        return QtCore.Qt.Orientations(QtCore.Qt.Orientation(0))
 
    def hasHeightForWidth(self):
        return True
 
    def heightForWidth(self, width):
        height = self.doLayout(QtCore.QRect(0, 0, width, 0), True)
        return height
 
    def setGeometry(self, rect):
        super(FlowLayout, self).setGeometry(rect)
        self.doLayout(rect, False)
 
    def sizeHint(self):
        return self.minimumSize()
 
    def minimumSize(self):
        size = QtCore.QSize()
 
        for item in self.itemList:
            size = size.expandedTo(item.minimumSize())
 
        margin = self.contentsMargins()
        size += QtCore.QSize(margin.left()+margin.right(), margin.top()+margin.bottom())
        return size
 
    def doLayout(self, rect, testOnly):
        x = rect.x()
        y = rect.y()
        lineHeight = 0
 
        for item in self.itemList:
            #wid = item.widget()
            spaceX = self.spacing()#+wid.style().layoutSpacing(QtWidgets.QSizePolicy.PushButton, QtWidgets.QSizePolicy.PushButton, QtCore.Qt.Horizontal)
            spaceY = self.spacing()#+wid.style().layoutSpacing(QtWidgets.QSizePolicy.PushButton, QtWidgets.QSizePolicy.PushButton, QtCore.Qt.Vertical)
            nextX = x + item.sizeHint().width() + spaceX
            if nextX - spaceX > rect.right() and lineHeight > 0:
                x = rect.x()
                y = y + lineHeight + spaceY
                nextX = x + item.sizeHint().width() + spaceX
                lineHeight = 0
 
            if not testOnly:
                item.setGeometry(QtCore.QRect(QtCore.QPoint(x, y), item.sizeHint()))
 
            x = nextX
            lineHeight = max(lineHeight, item.sizeHint().height())
 
        return y + lineHeight - rect.y()
