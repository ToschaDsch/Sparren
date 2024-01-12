import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QHBoxLayout, QPushButton, QLabel, QGridLayout, QTableWidget, QTableWidgetItem, QLineEdit
)
from PySide6 import QtGui

from variables import TextTranslation


class WindowSection(QMainWindow):
    def __init__(self):
        super().__init__()
        self._span_list: [float] = [3, 2.5]
        self._g3_list: [float] = [.3, .3]
        self._corner: float = 45
        left_layout = QVBoxLayout()
        self._make_left_layout(left_layout=left_layout)
        right_layout = QVBoxLayout()
        self._make_right_layout(right_layout=right_layout)
        up_layout = QHBoxLayout()
        up_layout.addLayout(left_layout)
        up_layout.addLayout(right_layout)


        bottom_layout = QGridLayout()

        general_layout = QVBoxLayout()
        general_layout.addLayout(up_layout)
        general_layout.addLayout(bottom_layout)
        widget = QWidget()
        widget.setLayout(general_layout)
        self.setCentralWidget(widget)

    def _make_left_layout(self, left_layout: QVBoxLayout):
        width = 90
        up_button_layout = QGridLayout()
        label_corner = QLabel(TextTranslation.corner.text)
        label_corner.setFixedWidth(width)
        up_button_layout.addWidget(label_corner, 0, 0)
        edit_corner = QLineEdit('45')
        edit_corner.setFixedWidth(width)
        edit_corner.textChanged.connect(self._corner_is_changed)
        up_button_layout.addWidget(edit_corner, 0, 1)
        button_plus = QPushButton('plus')
        button_plus.clicked.connect(self._plus_button)
        button_minus = QPushButton('minus')
        button_minus.clicked.connect(self._minus_a_span)

        up_button_layout.addWidget(button_plus, 1, 0)
        up_button_layout.addWidget(button_minus, 1, 1)

        left_layout.addLayout(up_button_layout)

        self._table = QTableWidget()
        self._table.setFixedWidth(200)
        header = [TextTranslation.span.text, 'g3, kN/m2']
        self._table.setColumnWidth(0, 60)
        self._table.setColumnWidth(1, 60)
        self._table.setColumnCount(len(header))
        self._table.setHorizontalHeaderLabels(header)
        self._table.setRowCount(len(self._span_list))
        self._table.itemChanged.connect(self._table_item_is_changed)
        left_layout.addWidget(self._table)
        for i, l_i in enumerate(self._span_list):
            self._table.setItem(i, 0, QTableWidgetItem(str(l_i)))
            self._table.setItem(i, 1, QTableWidgetItem(str(self._g3_list[i])))

    def _table_item_is_changed(self, item):
        row = item.row()
        col = item.column()
        text = item.text()
        try:
            i = abs(float(text))
        except TypeError:
            return None
        match col:
            case 0:
                self._span_list[row] = i
            case 1:
                self._g3_list[row] = i

    def _plus_button(self):
        self._span_list.append(self._span_list[-1])
        self._g3_list.append(self._g3_list[-1])
        self._add_a_span()

    def _minus_button(self):
        if len(self._span_list) == 1:
            return None
        self._span_list.pop()
        self._g3_list.pop()
        self._minus_a_span()

    def _corner_is_changed(self, text: str):
        try:
            i = abs(float(text))
        except TypeError:
            return None
        self._corner = i

    def _make_right_layout(self, right_layout: QVBoxLayout):
        self.label_for_canvas = QLabel()
        self.canvas = QtGui.QPixmap(200, 200)
        self.canvas.fill(Qt.GlobalColor.black)
        self.label_for_canvas.setPixmap(self.canvas)
        right_layout.addWidget(self.label_for_canvas)

        self.painter = QtGui.QPainter(self.canvas)
        brush = QtGui.QBrush(QtGui.QColor(33, 115, 70, 120))
        self.green_pen = QtGui.QPen(QtGui.QColor(33, 115, 70, 255), 5)
        self.yellow_pen = QtGui.QPen(QtGui.QColor(240, 230, 140, 255), 1)
        self.brown_pen = QtGui.QPen(QtGui.QColor(60, 60, 60, 255), 1)
        self.setFont(QtGui.QFont('Century Gothic', 10))
        self.painter.setBrush(brush)
        self.painter.setPen(self.green_pen)
        #self._scale = self.make_scale_for_preview()
        self.label_for_canvas.setMouseTracking(True)
        #self.calculate_new_coordinate_and_draw()

    def _add_a_span(self):
        current_row = self._table.rowCount()
        self._table.insertRow(current_row)

        self._table.setItem(current_row, 0, QTableWidgetItem(str(self._span_list[-1])))
        self._table.setItem(current_row, 1, QTableWidgetItem(str(self._g3_list[-1])))

    def _minus_a_span(self):
        i = self._table.rowCount() - 1
        self._table.removeRow(i)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WindowSection()
    window.show()
    app.exec()
