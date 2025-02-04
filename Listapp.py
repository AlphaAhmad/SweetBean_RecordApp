import sys
import qrcode
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPalette, QColor, QPixmap, QImage
from PyQt5.QtCore import Qt, QTimer, QDateTime, QSettings

# Global variables
headers = ["Product", "Quantity (Kg)", "Price (Rs)", "Actions"]

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sweet Bean")
        self.setGeometry(100, 100, 600, 500)

        # Main Layout
        self.MainLayout = QVBoxLayout()

        # Header Layout
        self.HeaderLayout = QHBoxLayout()

        # Meta Data Layout
        self.MetaData_Layout = QGridLayout()

        # Loading last invoice number
        self.settings = QSettings("Sweet Bean", "InvoiceApp")
        self.last_invoice_number = self.settings.value("last_invoice_number", 0, int)
        if self.last_invoice_number == 0:
            self.last_invoice_number = 1

        # Setting Up UI
        self.SetUp_UI()

        # Auto Date And Time Widget
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.UpdateTime)
        self.timer.start(1000)

    def SetUp_UI(self):
        # 1. Logo
        Logo_Label = QLabel()
        Logo = QPixmap("logo.jpeg")
        scaled_Logo = Logo.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        Logo_Label.setPixmap(scaled_Logo)
        Logo_Label.setAlignment(Qt.AlignCenter)
        self.MetaData_Layout.addWidget(Logo_Label, 0, 0, 1, 2)

        # 2. Date and Time
        self.dateTime_Label = QLabel()
        self.dateTime_Label.setAlignment(Qt.AlignCenter)
        self.MetaData_Layout.addWidget(self.dateTime_Label, 1, 0, 1, 2)

        # 3. Invoice and NTN
        self.Invoice_label = QLabel()
        self.Invoice_label.setAlignment(Qt.AlignCenter)
        self.update_Invoice_Widget()
        self.MetaData_Layout.addWidget(self.Invoice_label, 2, 0)

        self.NTN_label = QLineEdit()
        self.NTN_label.setPlaceholderText("Enter NTN number")
        self.MetaData_Layout.addWidget(self.NTN_label, 2, 1)

        # Input Fields & Add Button
        self.name_field = QLineEdit()
        self.name_field.setPlaceholderText("Product Name")

        self.quantity_Kgs = QSpinBox()
        self.quantity_Kgs.setRange(0, 100000000)
        self.quantity_Kgs.setPrefix("Kg ")

        self.Price_Rs = QSpinBox()
        self.Price_Rs.setRange(0, 1000000000)
        self.Price_Rs.setPrefix("Rs ")

        add_button = QPushButton("Add")
        add_button.clicked.connect(self.addRow)

        # Adding widgets to header layout
        self.HeaderLayout.addWidget(self.name_field)
        self.HeaderLayout.addWidget(self.quantity_Kgs)
        self.HeaderLayout.addWidget(self.Price_Rs)
        self.HeaderLayout.addWidget(add_button)

        # Table for product list
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(headers)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)

       # Layout for QR Codes
        self.QRLayout = QVBoxLayout()  # Changed to QVBoxLayout for proper vertical alignment

        # Sub-layout for QR images (horizontal)
        QRImagesLayout = QHBoxLayout()

        # Generate and display QR Codes
        facebook_qr = self.generate_qr("https://www.facebook.com/your_page")
        instagram_qr = self.generate_qr("https://www.instagram.com/your_profile")

        self.FB_QR_Label = QLabel()
        self.FB_QR_Label.setPixmap(self.qr_to_pixmap(facebook_qr))
        self.FB_QR_Label.setAlignment(Qt.AlignCenter)

        self.IG_QR_Label = QLabel()
        self.IG_QR_Label.setPixmap(self.qr_to_pixmap(instagram_qr))
        self.IG_QR_Label.setAlignment(Qt.AlignCenter)

        # Add QR images to the horizontal layout
        QRImagesLayout.addWidget(self.FB_QR_Label)
        QRImagesLayout.addWidget(self.IG_QR_Label)

        # Labels for QR indicating which one is for Facebook and Instagram
        fb_Label  = QLabel("Visit our Facebook")
        insta_Label  = QLabel("Visit our Instagram")

        fb_Label.setAlignment(Qt.AlignCenter)
        insta_Label.setAlignment(Qt.AlignCenter)

        # Sub-layout for QR labels (horizontal)
        QRLabelsLayout = QHBoxLayout()
        QRLabelsLayout.addWidget(fb_Label)
        QRLabelsLayout.addWidget(insta_Label)

        # Add both QR images and labels to the main QR layout
        self.QRLayout.addLayout(QRImagesLayout)
        self.QRLayout.addLayout(QRLabelsLayout)

        # Add layouts to main layout
        self.MainLayout.addLayout(self.MetaData_Layout)
        self.MainLayout.addLayout(self.HeaderLayout)
        self.MainLayout.addWidget(self.table)
        self.MainLayout.addLayout(self.QRLayout)  # Add QR Codes layout at the bottom

        # Set central widget
        container = QWidget()
        container.setLayout(self.MainLayout)
        self.setCentralWidget(container)

    # Function to generate QR Code
    def generate_qr(self, url):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=4,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        return qr.make_image(fill="black", back_color="white")

    # Convert QR to QPixmap for display
    def qr_to_pixmap(self, qr_img):
        qr_img = qr_img.convert("RGB")
        width, height = qr_img.size
        data = qr_img.tobytes("raw", "RGB")
        qimage = QImage(data, width, height, QImage.Format_RGB888)
        return QPixmap.fromImage(qimage)

    # Function to validate and add values into the table row
    def addRow(self):
        ProductName = self.name_field.text()
        ProductQuantity = self.quantity_Kgs.value()
        ProductPrice = self.Price_Rs.value()

        if not ProductName:
            QMessageBox.warning(self, "Error", "Product Name field is empty")
            return

        if not ProductQuantity:
            QMessageBox.warning(self, "Error", "Product Quantity field is empty")
            return

        if not ProductPrice:
            QMessageBox.warning(self, "Error", "Product Price field is empty")
            return

        row_index = self.table.rowCount()
        self.table.insertRow(row_index)

        self.table.setItem(row_index, 0, QTableWidgetItem(ProductName))
        self.table.setItem(row_index, 1, QTableWidgetItem(f"{ProductQuantity}"))
        self.table.setItem(row_index, 2, QTableWidgetItem(f"{ProductPrice}"))

        deleteButton = QPushButton("Delete")
        deleteButton.clicked.connect(lambda: self.deleteRow())
        self.table.setCellWidget(row_index, 3, deleteButton)

        self.name_field.clear()
        self.Price_Rs.setValue(0)
        self.quantity_Kgs.setValue(0)

    def deleteRow(self):
        button = self.sender()  # Get the button that was clicked
        if button:
            index = self.table.indexAt(button.pos())  # Find row from button position
            print(index.data)
            if index.isValid():
                self.table.removeRow(index.row())  # Delete the correct row
    
    def UpdateTime(self):
        current_date_time = QDateTime.currentDateTime().toString("dd-MM-yyyy  hh:mm:ss")
        self.dateTime_Label.setText(current_date_time)

    def update_Invoice_Widget(self):
        self.Invoice_label.setText(f"Invoice number: {self.last_invoice_number}")

    def closeEvent(self, event):
        self.settings.setValue("last_invoice_number", self.last_invoice_number)
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
