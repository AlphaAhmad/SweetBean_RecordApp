
import sys
from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDateTimeEdit,
    QDial,
    QDoubleSpinBox,
    QFontComboBox,
    QLabel,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSlider,
    QSpinBox,
    QTimeEdit,
    QMessageBox,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QWidget,
)

from PyQt5.QtGui import QPalette, QColor

# Global variables
headers = ["Product","Quantity (Kg)","Price (Rs)","Actions"]


class Color(QWidget):
    def __init__(self,color):
        super().__init__()
        
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sweet Bean")

        # Main Layout
        MainLayout = QVBoxLayout()

        # Layout for header where logo is present
        HeaderLayout = QHBoxLayout()

        # Input fields and add button 
        # 1. Product name
        self.name_field = QLineEdit()
        self.name_field.setPlaceholderText("Product Name")

        # 2. Product Quantity
        self.quantity_Kgs = QSpinBox()
        self.quantity_Kgs.setRange(0, 100000000)
        self.quantity_Kgs.setPrefix("Kg ")

        # 3. Product Price
        self.Price_Rs = QSpinBox()
        self.Price_Rs.setRange(0,1000000000)
        self.Price_Rs.setPrefix("Rs ")
        # self.Price_Rs.setPlaceholderText("Price")
        
        # Button to add into list
        add_button = QPushButton("Add")
        add_button.clicked.connect(self.addRow)

        # adding widgets to header layout
        HeaderLayout.addWidget(self.name_field)
        HeaderLayout.addWidget(self.quantity_Kgs)
        HeaderLayout.addWidget(self.Price_Rs)
        HeaderLayout.addWidget(add_button)

        # creating table layout for the scrollable list
        # making part of class since we will manipulate it using add function
        self.table = QTableWidget()
        self.table.setColumnCount(4) 
        self.table.setHorizontalHeaderLabels(headers)
        self.table.horizontalHeader().setStretchLastSection(True) # Make final column fill all remain space
        self.table.verticalHeader().setVisible(False) # making numbering of rows invisible

        # adding both of these in the main layout

        MainLayout.addLayout(HeaderLayout)
        MainLayout.addWidget(self.table)

        # Central widget
        container = QWidget()
        container.setLayout(MainLayout)
        self.setCentralWidget(container)


    ## Now adding fuctions
    
    # function to validate or add values into the table row
    def addRow(self):
        ProductName = self.name_field.text()
        ProductQuantity = self.quantity_Kgs.value() 
        ProductPrice = self.Price_Rs.value()

        # Validation and Error throwing 
        if not ProductName :
            QMessageBox.warning(self,"Error","Product Name field is empty")
            return 
        
        if not ProductQuantity: 
            QMessageBox.warning(self,"Error","Product Quantity field is empty")
            return 

        if not ProductPrice:
            QMessageBox.warning(self,"Error","Product Price field is empty")
            return 
        
        # Now adding row to the table   
        row_index = self.table.rowCount() # getting the number of the row where it will be inserted (like index)
        self.table.insertRow(row_index) # adding an empty row at that index
            
            # Now populating data in that row
        self.table.setItem(row_index,0,QTableWidgetItem(ProductName))
        self.table.setItem(row_index,1,QTableWidgetItem(f"{ProductQuantity}"))
        self.table.setItem(row_index,2,QTableWidgetItem(f"{ProductPrice}"))

            # Now adding a delete button at the end of each row
        deleteButton = QPushButton("Delete")
        deleteButton.clicked.connect(lambda:self.deleteRow(row_index))
        self.table.setCellWidget(row_index,3,deleteButton)
        
        # clearing the input fields
        self.name_field.clear()
        self.Price_Rs.setValue(0)
        self.quantity_Kgs.setValue(0)

    def deleteRow(self,row):
        self.table.removeRow(row)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
