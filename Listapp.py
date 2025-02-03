import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPalette, QColor, QPixmap
from PyQt5.QtCore import Qt, QTimer, QDateTime, QSettings

# Global variables
headers = ["Product", "Quantity (Kg)", "Price (Rs)", "Actions"]


class Color(QWidget):
    def __init__(self, color):
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
        self.MainLayout = QVBoxLayout()

        # Layout for header where logo is present
        self.HeaderLayout = QHBoxLayout()

        # Meta Data Layout (Logo, date, time, NTN, Invoice)
        self.MetaData_Layout = QGridLayout()

        # Loading last invoice number
        self.settings = QSettings("Sweet Bean", "InvoiceApp")
        self.last_invoice_number = self.settings.value("last_invoice_number", 0, int)
        if self.last_invoice_number == 0:
            self.last_invoice_number = 1  # Initialize to 1 if no saved invoice number exists

        # Setting Up UI
        self.SetUp_UI()

        # Auto Date And Time Widget
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.UpdateTime)  # Timeout is a signal that runs every second
        self.timer.start(1000)  # Every second

    # UI Setting
    def SetUp_UI(self):
        # +++++ 1. Logo in the top row
        Logo_Label = QLabel()  # Widget to show image and text
        Logo = QPixmap("logo.jpeg")
        scaled_Logo = Logo.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        Logo_Label.setPixmap(scaled_Logo)
        Logo_Label.setAlignment(Qt.AlignCenter)
        # Spanning the logo in the 0th row and 1st and 2nd column to show it in the center
        self.MetaData_Layout.addWidget(Logo_Label, 0, 0, 1, 2)

        # ++++ 2. Date and time in the second row
        self.dateTime_Label = QLabel()
        self.dateTime_Label.setAlignment(Qt.AlignCenter)
        self.MetaData_Layout.addWidget(self.dateTime_Label, 1, 0, 1, 2)

        # ++++ 3. Invoice and NTN in 3rd row
        self.Invoice_label = QLabel()
        self.Invoice_label.setAlignment(Qt.AlignCenter)
        self.update_Invoice_Widget()  # Initialize the invoice label
        self.MetaData_Layout.addWidget(self.Invoice_label, 2, 0)

        self.NTN_label = QLineEdit()
        self.NTN_label.setPlaceholderText("Enter NTN number")
        self.MetaData_Layout.addWidget(self.NTN_label, 2, 1)

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
        self.Price_Rs.setRange(0, 1000000000)
        self.Price_Rs.setPrefix("Rs ")

        # Button to add into list
        add_button = QPushButton("Add")
        add_button.clicked.connect(self.addRow)

        # Adding widgets to header layout
        self.HeaderLayout.addWidget(self.name_field)
        self.HeaderLayout.addWidget(self.quantity_Kgs)
        self.HeaderLayout.addWidget(self.Price_Rs)
        self.HeaderLayout.addWidget(add_button)

        # Creating table layout for the scrollable list
        # Making part of class since we will manipulate it using add function
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(headers)
        self.table.horizontalHeader().setStretchLastSection(True)  # Make final column fill all remaining space
        self.table.verticalHeader().setVisible(False)  # Making numbering of rows invisible

        # Adding both of these in the main layout
        self.MainLayout.addLayout(self.MetaData_Layout)
        self.MainLayout.addLayout(self.HeaderLayout)
        self.MainLayout.addWidget(self.table)

        # Central widget
        container = QWidget()
        container.setLayout(self.MainLayout)
        self.setCentralWidget(container)

    # ++++++++++++++++++++++++++++++
    ## --- Class functions/Methods --- ##
    # ++++++++++++++++++++++++++++++

    # Function to validate and add values into the table row
    def addRow(self):
        ProductName = self.name_field.text()
        ProductQuantity = self.quantity_Kgs.value()
        ProductPrice = self.Price_Rs.value()

        # Validation and Error throwing
        if not ProductName:
            QMessageBox.warning(self, "Error", "Product Name field is empty")
            return

        if not ProductQuantity:
            QMessageBox.warning(self, "Error", "Product Quantity field is empty")
            return

        if not ProductPrice:
            QMessageBox.warning(self, "Error", "Product Price field is empty")
            return

        # Now adding an empty row to the table
        row_index = self.table.rowCount()  # Getting the number of the row where it will be inserted (like index)
        self.table.insertRow(row_index)  # Adding an empty row at that index

        # Now populating data in that row
        self.table.setItem(row_index, 0, QTableWidgetItem(ProductName))
        self.table.setItem(row_index, 1, QTableWidgetItem(f"{ProductQuantity}"))
        self.table.setItem(row_index, 2, QTableWidgetItem(f"{ProductPrice}"))

        # Now adding a delete button at the end of each row
        deleteButton = QPushButton("Delete")
        deleteButton.clicked.connect(lambda: self.deleteRow(row_index))
        self.table.setCellWidget(row_index, 3, deleteButton)

        # Clearing the input fields
        self.name_field.clear()
        self.Price_Rs.setValue(0)
        self.quantity_Kgs.setValue(0)

        # Increment the invoice number after adding a row
        self.last_invoice_number += 1
        self.update_Invoice_Widget()

    def deleteRow(self, row):
        self.table.removeRow(row)

    def UpdateTime(self):
        # Taking current date and time
        current_date_time = QDateTime.currentDateTime().toString("dd-MM-yyyy  hh:mm:ss")

        # Updating text in date time widget (label) we created in SetUp_UI
        self.dateTime_Label.setText(current_date_time)

    def update_Invoice_Widget(self):
        # Update the invoice label with the current invoice number
        self.Invoice_label.setText(f"Invoice number: {self.last_invoice_number}")

    def closeEvent(self, event):
        # Save the last invoice number when the application closes
        self.settings.setValue("last_invoice_number", self.last_invoice_number)
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())