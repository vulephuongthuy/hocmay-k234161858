import sys
import pickle
import pandas as pd
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow

from ui.HousingPricePredictionMainWindow import Ui_MainWindow


class HousingPricePredictionMainWindowEx(Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.model = None
        self.is_completed = False

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.load_model()
        self.setupSignalAndSlot()
        self.is_completed = True

    def load_model(self):
        modelname = "housingmodel.zip"
        try:
            with open(modelname, "rb") as f:
                self.model = pickle.load(f)
            print("✅ Model loaded successfully!")
        except Exception as e:
            print(f"⚠️ Error loading model: {e}")
            self.model = None

    def setupSignalAndSlot(self):
        self.pushButtonPredict.clicked.connect(self.predict_price)

    def get_input_data(self):
        try:
            avg_income = float(self.lineEditAvgAreaIncome.text())
            avg_house_age = float(self.lineEditAvgAreaHouseAge.text())
            avg_rooms = float(self.lineEditAvgAreaNumberofRooms.text())
            avg_bedrooms = float(self.lineEditAvgAreaNumberofBedrooms.text())
            area_population = float(self.lineEditAreaPopulation.text())

            data = pd.DataFrame([[
                avg_income,
                avg_house_age,
                avg_rooms,
                avg_bedrooms,
                area_population
            ]], columns=[
                'Avg. Area Income',
                'Avg. Area House Age',
                'Avg. Area Number of Rooms',
                'Avg. Area Number of Bedrooms',
                'Area Population'
            ])
            return data

        except ValueError:
            QtWidgets.QMessageBox.warning(
                self.MainWindow, "Input Error", "Vui lòng nhập số hợp lệ cho tất cả các ô!"
            )
            return None

    def predict_price(self):
        if not self.model:
            QtWidgets.QMessageBox.critical(self.MainWindow, "Error", "Model chưa được tải!")
            return

        data = self.get_input_data()
        if data is None:
            return

        try:
            prediction = self.model.predict(data)[0]
            self.labelPredict.setText(f"{prediction:,.2f} USD")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self.MainWindow, "Error", f"Lỗi khi dự đoán: {e}")

    def showWindow(self):
        self.MainWindow.show()


# ---------------- Example ----------------
if __name__ == "__main__":
    app = QApplication([])
    main_window = QMainWindow()
    pricing_ui = HousingPricePredictionMainWindowEx()
    pricing_ui.setupUi(main_window)
    main_window.show()
    app.exec()

