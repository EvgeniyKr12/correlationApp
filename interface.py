import sys
from main import analysis
from matplotlib.figure import Figure
from PySide6 import QtCore, QtWidgets, QtGui
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class MyWidget(QtWidgets.QWidget):
    ''' Класс для окна ввода информации'''
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Regression analysis')

        # Создание окна
        self.layout = QtWidgets.QVBoxLayout(self)
        self.setLayout(self.layout)
        self.layout.addStretch()

        # Подключение шрифтов
        font_id = QtGui.QFontDatabase.addApplicationFont("Roboto/Roboto-Bold.ttf")
        font_family = QtGui.QFontDatabase.applicationFontFamilies(font_id)[0]

        # Отображение заголовка
        self.label = QtWidgets.QLabel("Регрессионный анализ")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setStyleSheet(f"color: purple; font-size: 24px; font-family: {font_family}; font-weight: bold")
        self.layout.addWidget(self.label)

        # Поле ввода X
        h_layout1 = QtWidgets.QHBoxLayout()
        self.input1 = QtWidgets.QLineEdit(self)
        self.input1.setPlaceholderText("Введите x через пробел")
        self.input1.setFixedSize(400, 30)
        h_layout1.addWidget(self.input1)
        self.layout.addLayout(h_layout1)

        # Поле ввода Y
        h_layout2 = QtWidgets.QHBoxLayout()
        self.input2 = QtWidgets.QLineEdit(self)
        self.input2.setPlaceholderText("Введите y через пробел")
        self.input2.setFixedSize(400, 30)
        h_layout2.addWidget(self.input2)
        self.layout.addLayout(h_layout2)

        # Кнопка отправить
        h_layout3 = QtWidgets.QHBoxLayout()
        self.button = QtWidgets.QPushButton("Отправить", self)
        self.button.setFixedSize(400, 30)
        h_layout3.addWidget(self.button)
        self.layout.addLayout(h_layout3)
        self.layout.addStretch()

        # Тригер кнопки
        self.button.clicked.connect(self.get_inputs)



    def get_inputs(self):
        ''' Функция которая срабатывает при  нажатии на кнопку `Отправить` '''
        x_list = [int(i) for i in self.input1.text().split(' ')]
        y_list = [int(i) for i in self.input2.text().split(' ')]

        result = analysis(x_list, y_list)

        # Откритие новых окон для вывода результата
        self.new_window_result = ResultWindow(result)
        self.new_window_result.show()

        self.new_window_table = TableWindow(result)
        self.new_window_table.show()

        self.close()

class TableWindow(QtWidgets.QWidget):
    ''' Класс для вывода таблицы'''
    def __init__(self, result):
        super().__init__()
        self.setWindowTitle('Regression analysis')
        self.resize(550, 700)
        layout = QtWidgets.QVBoxLayout(self)
        self.setLayout(layout)

        # Генерируем таблицу
        length = len(result['x_list']) + 1
        table = QtWidgets.QTableWidget()
        table.setColumnCount(5)
        table.setRowCount(length)

        # Прописываем заголовки
        table.setHorizontalHeaderLabels(["X", "Y", "X^2", "XY", "Y^2"])
        row_labels = [str(i) for i in range(1, length)]
        row_labels.append('Σ')
        table.setVerticalHeaderLabels(row_labels)

        # Запоняем таблицу
        for i, (x_list, y_list, squared_x, xy_list, squared_y) in enumerate(zip(result['x_list'], result['y_list'], result['squared_x'], result['xy_list'], result['squared_y'])):
            table.setItem(i, 0, QtWidgets.QTableWidgetItem(str(x_list)))
            table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(y_list)))
            table.setItem(i, 2, QtWidgets.QTableWidgetItem(str(squared_x)))
            table.setItem(i, 3, QtWidgets.QTableWidgetItem(str(xy_list)))
            table.setItem(i, 4, QtWidgets.QTableWidgetItem(str(squared_y)))

        for i, sum_value in enumerate(result['sum_list']):
            table.setItem(length - 1, i, QtWidgets.QTableWidgetItem(str(sum_value)))

        layout.addWidget(table)


class ResultWindow(QtWidgets.QWidget):
    '''Класс для вывода результатов '''
    def __init__(self, result):
        super().__init__()
        self.setWindowTitle('Regression analysis')
        self.resize(600, 700)
        layout = QtWidgets.QVBoxLayout(self)
        self.setLayout(layout)

        # Подключение шрифтов
        font_id = QtGui.QFontDatabase.addApplicationFont("Roboto/Roboto-Bold.ttf")
        font_family = QtGui.QFontDatabase.applicationFontFamilies(font_id)[0]

        # Отображение заголовка
        self.label = QtWidgets.QLabel("Регрессионный анализ")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setStyleSheet(f"color: purple; font-size: 24px; font-family: {font_family}; font-weight: bold")
        layout.addWidget(self.label)

        font_id = QtGui.QFontDatabase.addApplicationFont("Roboto/Roboto-Medium.ttf")
        font_family = QtGui.QFontDatabase.applicationFontFamilies(font_id)[0]

        h_layout = QtWidgets.QHBoxLayout()
        layout.addLayout(h_layout)

        # Создание графиков
        h_layout.addWidget(self.get_canvas(result['x_list'], result['y_list'], 'o'), alignment=QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        h_layout.addWidget(self.get_canvas(result['a_list'], result['b_list'], '-'), alignment=QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)

        # Отступ
        spacer = QtWidgets.QSpacerItem(10, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        layout.addItem(spacer)

       # Вывод всех расчетов
        average_label = QtWidgets.QLabel()
        average_label.setAlignment(QtCore.Qt.AlignLeft)
        average_label.setStyleSheet(f"color: white; font-size: 18px; font-family: {font_family};")
        average_string = f' Σx/n = {result["average_x_list"]} \n Σy/n = {result["average_y_list"]} \n Σx^2/n = {result["average_squared_x"]} \n Σxy/n = {result["average_xy_list"]} \n Σy^2/n = {result["average_squared_y"]}'
        average_label.setText(average_string)

        r_label = QtWidgets.QLabel()
        r_label.setAlignment(QtCore.Qt.AlignLeft)
        r_label.setStyleSheet(f"color: white; font-size: 18px; font-family: {font_family};")
        r_string = f' K* = {result["k_xy"]} \n σx = {result["sigma_x"]} \n σy = {result["sigma_y"]} \n R= {result["r"]}'
        r_label.setText(r_string)

        h_text_layout = QtWidgets.QHBoxLayout()
        h_text_layout.addWidget(average_label, alignment=QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        h_text_layout.addWidget(r_label, alignment=QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        layout.addLayout(h_text_layout)

        # Отступ
        spacer = QtWidgets.QSpacerItem(10, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        layout.addItem(spacer)

        # Вывод изображения системы
        image_label = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap("system.png")
        scaled_pixmap = pixmap.scaled(270, 150)
        image_label.setPixmap(scaled_pixmap)

        system_label = QtWidgets.QLabel()
        system_label.setAlignment(QtCore.Qt.AlignLeft)
        system_label.setStyleSheet(f"color: white; font-size: 18px; font-family: {font_family};")
        system_string = f"\nСогласно системе получим:\na = {result['a']}, а b = {result['b']} \n \nУуравнение регрессии имеет вид:\ny = {result['b']} + {result['a']}x"
        system_label.setText(system_string)


        h_system_layout = QtWidgets.QHBoxLayout()
        h_system_layout.addWidget(image_label, alignment=QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        h_system_layout.addWidget(system_label, alignment=QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        layout.addLayout(h_system_layout)

        spacer = QtWidgets.QSpacerItem(10, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        layout.addItem(spacer)

    def get_canvas(self, list1, list2, type):
        '''Функция для построения графиков'''
        fig = Figure(figsize=(0.7, 0.7))
        fig.patch.set_facecolor('#1e1e1e')
        canvas = FigureCanvas(fig)
        canvas.setFixedSize(300, 300)

        ax = fig.add_subplot(111)
        ax.plot(list1, list2, type, color='purple')
        ax.set_facecolor('#1e1e1e')
        ax.spines['bottom'].set_color('white')
        ax.spines['top'].set_color('#1e1e1e')
        ax.spines['left'].set_color('white')
        ax.spines['right'].set_color('#1e1e1e')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')

        return canvas



if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = MyWidget()
    widget.resize(700, 500)
    widget.show()
    sys.exit(app.exec())
