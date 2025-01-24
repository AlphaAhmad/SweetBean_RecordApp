import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow
from PyQt5.QtCore import QSize,Qt

# Variables
AppName = "Sweet Bean"
Width , Height = 1000 , 900

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self): 
        super().__init__()

        self.setWindowTitle(AppName)
        button = QPushButton("Press Me!")
        # Set the central widget of the Window.
        self.setFixedSize(QSize(Width,Height))
        self.setCentralWidget(button)
        


app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()
