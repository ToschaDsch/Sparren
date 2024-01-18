import math
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

from variables import TextTranslation, Variables


class WindowSection(QMainWindow):
    def __init__(self):
        super().__init__()
        # init class variables
        self._span_list: [float] = [3, 2.5]
        self._g3_list: [float] = [.3, .3]
        self._corner: float = 45
        self._scale: float = 1
        self._alpha: float = math.pi * .25
        self._console: float = 0.7

        # init frontend elements
        self._painter: QtGui.QPainter | None = None
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

        bottom_layout = QHBoxLayout()
        label_console = QLabel(TextTranslation.console.text)
        bottom_layout.addWidget(label_console)
        edit_console = QLineEdit('0.7')
        edit_console.setFixedWidth(width)
        edit_console.textChanged.connect(self._console_is_changed)
        bottom_layout.addWidget(edit_console)
        left_layout.addLayout(bottom_layout)

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
        self._draw_all()

    def _minus_button(self):
        if len(self._span_list) == 1:
            return None
        self._span_list.pop()
        self._g3_list.pop()
        self._minus_a_span()
        self._draw_all()

    def _corner_is_changed(self, text: str):
        if text == '':
            return None
        try:
            i = abs(float(text))
        except TypeError:
            return None
        if i > 90:
            i = 89
        self._corner = i
        self._draw_all()

    def _console_is_changed(self, text: str):
        try:
            i = abs(float(text))
        except TypeError:
            return None
        self._console = i
        self._draw_all()

    def _make_right_layout(self, right_layout: QVBoxLayout):
        self.label_for_canvas = QLabel()
        self.canvas = QtGui.QPixmap(Variables.screenBH[0], Variables.screenBH[1])
        self.canvas.fill(Qt.GlobalColor.black)
        self.label_for_canvas.setPixmap(self.canvas)
        right_layout.addWidget(self.label_for_canvas)

        self.painter = QtGui.QPainter(self.canvas)
        brush = QtGui.QBrush(QtGui.QColor(33, 115, 70, 120))
        self.green_pen = QtGui.QPen(QtGui.QColor(33, 115, 70, 255), 1)
        self.yellow_pen = QtGui.QPen(QtGui.QColor(240, 230, 140, 255), 1)
        self.brown_pen = QtGui.QPen(QtGui.QColor(60, 60, 60, 255), 1)
        self.setFont(QtGui.QFont('Century Gothic', 10))
        self.painter.setBrush(brush)
        self.painter.setPen(self.green_pen)
        self.label_for_canvas.setMouseTracking(True)
        self._draw_all()

    def _draw_all(self):
        self.canvas.fill(Qt.GlobalColor.black)
        self._draw_model()
        self.label_for_canvas.setPixmap(self.canvas)

    def _draw_model(self):
        self._calculate_scale()
        #self._draw_axes()
        self._draw_spans()

    def _draw_spans(self):

        # draw_a_console
        x_i = 0
        y_i = 0
        x_i_1 = x_i + self._console / math.cos(self._alpha)
        y_i_1 = y_i + self._console / math.sin(self._alpha)
        self._draw_a_span(x1=x_i, y1=y_i, x2=x_i_1, y2=y_i_1, support_at_the_beginning=False)
        x_i = x_i_1
        y_i = y_i_1
        for l_i in self._span_list:
            x_i_1 = x_i + l_i / math.cos(self._alpha)
            y_i_1 = y_i + l_i / math.sin(self._alpha)
            self._draw_a_span(x1=x_i, y1=y_i, x2=x_i_1, y2=y_i_1)
            x_i = x_i_1
            y_i = y_i_1

    def _draw_a_span(self, x1: float, y1: float, x2: float, y2: float,
                     support_at_the_beginning: bool = True,
                     support_at_the_end: bool = True, ):
        self.painter.setPen(self.green_pen)
        # draw a span
        self._draw_line(x1=x1, y1=y1, x2=x2, y2=y2)
        # draw a support
        if support_at_the_beginning:
            self._draw_line(x1=x1, y1=y1, x2=x1, y2=y1 - .5)
        if support_at_the_end:
            self._draw_line(x1=x2, y1=y2, x2=x2, y2=y2 - .5)
        self.painter.setPen(self.brown_pen)
        # draw size line
        # vertical
        self._draw_line(x1=x1, y1=y1 - 1, x2=x1, y2=-1)
        self._draw_line(x1=x2, y1=y2 - 1, x2=x2, y2=-1)
        # horizontal
        self._draw_line(x1=x1-.2, y1=-.8, x2=x2+.2, y2=-.8)
        # diagonal
        self._draw_line(x1=x1 - .2, y1=-.8+.2, x2=x1 + .2, y2=-.8-.2)
        self._draw_line(x1=x2 - .2, y1=-.8+.2, x2=x2 + .2, y2=-.8-.2)

    def _calculate_scale(self):
        sl = 0
        for l_i in self._span_list:
            sl += l_i
        self._alpha = self._corner * math.pi / 180
        sl += self._console
        lx = sl / math.cos(self._alpha)
        ly = sl / math.sin(self._alpha)
        space_x = Variables.screenBH[0] - Variables.screen_space_x0 - Variables.screen_space_xn
        scale_x = space_x / lx
        space_y = Variables.screenBH[1] - Variables.screen_space_y0 - Variables.screen_space_yn
        scale_y = space_y / ly
        self._scale = min(scale_x, scale_y)

    def _draw_axes(self):
        self.painter.setPen(self.brown_pen)
        # horizontal axis
        self.painter.drawLine(Variables.screen_space_x0 - 5,
                              Variables.screenBH[1] - Variables.screen_space_y0,
                              Variables.screenBH[0] - Variables.screen_space_xn,
                              Variables.screenBH[1] - Variables.screen_space_y0)
        # vertical axis
        self.painter.drawLine(Variables.screen_space_x0,
                              Variables.screenBH[1] - Variables.screen_space_y0 + 5,
                              Variables.screen_space_x0,
                              Variables.screen_space_y0)

    def _draw_line(self, x1: float, x2: float, y1: float, y2: float):
        x1 = self._scale * x1 + Variables.screen_space_x0
        y1 = -self._scale * y1 + Variables.screenBH[1] - Variables.screen_space_y0
        x2 = self._scale * x2 + Variables.screen_space_x0
        y2 = -self._scale * y2 + Variables.screenBH[1] - Variables.screen_space_y0
        self.painter.drawLine(x1, y1, x2, y2)

    def draw_text(self, text: str, x_y: tuple[float]):
        x = self._scale * x_y[0] + Variables.screen_space_x0
        y = -self._scale * x_y[1] + Variables.screenBH[1] - Variables.screen_space_y0
        self.painter.drawText(x, y, text)

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
