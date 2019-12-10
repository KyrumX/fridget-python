import sys

from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtWidgets import QTableWidgetItem

from platform_wrapper.models.products import Products
from platform_wrapper.platform_wrapper import PlatformWrapper


class MainWindow(QtWidgets.QMainWindow):

    products = Products()

    def __init__(self, platform_api: PlatformWrapper, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("resources/ui/stackedTest.ui", self)

        self.platform_api = platform_api

        self.stacked_widget = self.findChild(QtWidgets.QStackedWidget, 'stackedWidget')
        self.stacked_widget.setCurrentIndex(0)
        self.p1 = self.stacked_widget.findChild(QtWidgets.QWidget, 'p1')
        self.p2 = self.stacked_widget.findChild(QtWidgets.QWidget, 'p2')
        self.button = self.p1.findChild(QtWidgets.QPushButton, 'p1ChangePage2Button')
        self.button.clicked.connect(self.switch_to_second_screen)
        self.button2 = self.p1.findChild(QtWidgets.QPushButton, 'changeImgButton')
        self.button2.clicked.connect(self.change_image)
        self.label = self.p1.findChild(QtWidgets.QLabel, 'label1')
        self.table = self.p2.findChild(QtWidgets.QTableWidget, 'tableWidget')
        self.button39 = self.p2.findChild(QtWidgets.QPushButton, 'pushButton39')
        self.button39.clicked.connect(self.add_to_table)
        self.sendProductsButton = self.p2.findChild(QtWidgets.QPushButton, 'sendProductsButton')
        self.sendProductsButton.clicked.connect(self.send_products_to_box)

        #self.showFullScreen()
        self.show()

    def switch_to_second_screen(self):
        self.stacked_widget.setCurrentIndex(1)

    def change_image(self):
        pixmap = QtGui.QPixmap("077G.png")
        #self.label.setPixmap(pixmap)

        url = 'http://www.google.com/images/srpr/logo1w.png'
        import urllib.request
        data = urllib.request.urlopen(url).read()

        image = QtGui.QImage()
        image.loadFromData(data)

        self.label.setPixmap(QtGui.QPixmap(image))

    def add_to_table(self):
        from platform_wrapper.models.product import Product

        import datetime
        product = Product(product_name="Coca Cola 1L", product_desc="Vles Coca Cola van 1 liter", product_amount=1, product_amount_unit="liters", product_exp=datetime.datetime(2020, 5, 17).date())
        self.products.add_product(product)

        rowPosition = self.table.rowCount()
        self.table.insertRow(rowPosition)
        self.table.setItem(rowPosition, 0, QTableWidgetItem(product.product_name))
        self.table.scrollToBottom()

    def send_products_to_box(self):
        self.platform_api.add_products(self.products)

platform_api = PlatformWrapper(api_key="")

app = QtWidgets.QApplication(sys.argv)
window = MainWindow(platform_api)
# window.showFullScreen()
sys._excepthook = sys.excepthook
def exception_hook(exctype, value, traceback):
    print(exctype, value, traceback)
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)
sys.excepthook = exception_hook

app.exec_()