import os 
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QDialog, QVBoxLayout, QTextEdit, QDesktopWidget, QRadioButton, QButtonGroup
from PyQt5.QtGui import QPalette, QColor, QPixmap, QFont
from PyQt5.QtCore import Qt

# class for switch button
class PowerSwitch(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(60, 30)
        self.setCheckable(True)
        self.setText("OFF")
        self.setStyleSheet(self.get_style(False))
        self.clicked.connect(self.toggle_style)

    def get_style(self, checked):
        return f"""
        QPushButton {{
            background-color: {'#6A6F4C' if checked else '#E5E5E5'};
            border: #5F6368;
            border-radius: 15px;
            color: {'#FFFFFF' if checked else '#5F6368'};
            font-weight: bold;
        }}
        """

    ## switching on and off power button
    def toggle_style(self):
        self.setStyleSheet(self.get_style(self.isChecked()))
        self.setText("ON" if self.isChecked() else "OFF")

# class for logs
class LogDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Logs')
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)
        self.resize(parent.size())
        self.setMinimumSize(400, 300)
        layout = QVBoxLayout()
        self.text_edit = QTextEdit(self)
        layout.addWidget(self.text_edit)
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.icon_path = os.path.join(os.path.dirname(__file__), 'icons') # absolute path
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Dont Wrist It')
        self.setFixedSize(500, 300)
        self.setPalette(QPalette(QColor("#828E82")))

        #switch on off
        self.power = PowerSwitch(self)
        self.power.setGeometry(420, 20, 60, 30)

        self.hand_posture_guidelines() # guidelines
        self.add_buttons_and_labels()   #view log
        self.add_radio_buttons()    #button for alert mechanism

        desktop = QDesktopWidget()
        screenRect = desktop.screenGeometry()
        windowRect = self.geometry()
        self.move(screenRect.width() - windowRect.width() - 15, screenRect.height() - windowRect.height() - 105)

    ## for correct and inccorect guidelsines of hand posture
    def hand_posture_guidelines(self):
        # square boxes
        self.big_square = QLabel(self)
        self.big_square.setGeometry(15, 60, 180, 220)
        self.big_square.setStyleSheet("background-color: #F9EBC7; border-radius: 7px;")  # correct hand posture
        self.big_square = QLabel(self)
        self.big_square.setGeometry(205, 60, 180, 220)
        self.big_square.setStyleSheet("background-color: #F9EBC7; border-radius: 7px;") # incorrect hand posture

        # contents of the boxes (inlucdes labels and images)
        self.createLabel("Correct Hand Posture", 37, 70, "black", 15, QFont.Bold, 180)
        self.createLabel("Incorrect Hand Posture", 222, 70, "black", 15, QFont.Bold, 180)
        self.createPixmapLabel('good1.png', 30, 60, 150, 150)
        self.createPixmapLabel('good2.png', 40, 160, 130, 130)
        self.createPixmapLabel('bad1.png', 210, 55, 170, 170)
        self.createPixmapLabel('bad2.png', 242, 170, 110, 110)

    def add_buttons_and_labels(self):
        self.createLabel("Don't Wrist It", 65, 15, "white", 15, QFont.Bold)
        self.createLabel("Choose your alert", 395, 170, "white", 12, QFont.Bold)
        self.createPixmapLabel('logo.png', 10, 5, 50, 50)

        button = QPushButton('View Logs', self)
        button.setGeometry(395, 110, 100, 30)
        button.setStyleSheet("background-color: #B99470; border-radius: 5px;")
        button.clicked.connect(self.show_logs)

    def add_radio_buttons(self):
        radio_button1 = QRadioButton("Audio Cue", self)
        radio_button2 = QRadioButton("Visual Cue", self)
        radio_button1.setGeometry(395, 200, 100, 30)
        radio_button2.setGeometry(395, 230, 100, 30)
        radio_group = QButtonGroup(self)
        radio_group.addButton(radio_button1)
        radio_group.addButton(radio_button2)

    def createLabel(self, text, x, y, color, size, weight, width=180):
        label = QLabel(text, self)
        label.setGeometry(x, y, width, 30)
        label.setStyleSheet(f"color: {color}; font-size: {size}px; font-weight: {weight};")

    def createPixmapLabel(self, filename, x, y, width, height):
        pixmap_path = os.path.join(self.icon_path, filename) # absolute path
        label = QLabel(self)
        pixmap = QPixmap(pixmap_path).scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        label.setPixmap(pixmap)
        label.setGeometry(x, y, width, height)

    def show_logs(self):
        dialog = LogDialog(self)
        dialog.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())