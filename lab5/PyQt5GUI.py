import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout

class SimplePyQtApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Простой PyQt5 GUI')
        self.setGeometry(300, 300, 300, 200)

        layout = QVBoxLayout()

        self.label = QLabel('Добро пожаловать в PyQt5!')
        self.button = QPushButton('Нажми меня!')

        self.button.clicked.connect(self.on_button_click)

        layout.addWidget(self.label)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def on_button_click(self):
        self.label.setText('Кнопка была нажата!')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SimplePyQtApp()
    window.show()
    sys.exit(app.exec_())
