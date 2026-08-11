import sys
from PyQt6 import QtWidgets, QtCore
from rental import Ui_MainWindow
from koneksi_db import connect_db, init_db
from member import PanelMember
from membership import PanelMembership
from transaksi import TransaksiController

class CustomMessageBox:
    def __init__(self, title, message, parent=None):
        self.dialog = QtWidgets.QDialog(parent)
        self.dialog.setWindowTitle(title)
        self.dialog.setFixedSize(350, 150)
        self.dialog.setStyleSheet("""
            QDialog {
                background: #2F353B;
                color: #F2F4F5;
                font-family: 'Segoe UI';
                border: 2px solid #4B5663;
                border-radius: 6px;
            }
            QLabel {
                color: #F2F4F5;
                font-size: 14px;
                background: transparent;
            }
            QLabel#lblTitle {
                color: #00FFE5;
                font-size: 16px;
                font-weight: bold;
                margin-bottom: 10px;
            }
            QPushButton {
                background: #262A2E;
                border: 2px solid #00FFE5;
                color: #00FFE5;
                min-height: 30px;
                min-width: 80px;
                font-weight: bold;
                border-radius: 4px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background: #374049;
            }
        """)
        
        self.dialog.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint | QtCore.Qt.WindowType.Dialog)
        layout = QtWidgets.QVBoxLayout(self.dialog)
        layout.setContentsMargins(20, 20, 20, 20)
        self.lbl_title = QtWidgets.QLabel(title)
        self.lbl_title.setObjectName("lblTitle")
        self.lbl_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.lbl_title)
        self.lbl_msg = QtWidgets.QLabel(message)
        self.lbl_msg.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lbl_msg.setWordWrap(True)
        layout.addWidget(self.lbl_msg)
        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.btn_ok = QtWidgets.QPushButton("OK")
        self.btn_ok.clicked.connect(self.dialog.accept)
        btn_layout.addWidget(self.btn_ok)
        layout.addLayout(btn_layout)
        
    def exec(self):
        return self.dialog.exec()

    @staticmethod
    def show_message(parent, title, message):
        msg_box = CustomMessageBox(title, message, parent)
        msg_box.exec()

class MainApp:
    def __init__(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.window)
        self.ui.btnGoDashboard.clicked.connect(self.go_to_dashboard)
        self.ui.btnBukanAdmin.clicked.connect(self.bukan_admin_exit)
        self.ui.actionLanding_Page.triggered.connect(self.go_to_landing)
        self.ui.actionDashboard.triggered.connect(self.go_to_dashboard)
        self.ui.actionMembership.triggered.connect(self.go_to_membership)
        self.ui.actionTransaksi.triggered.connect(self.go_to_transaksi)
        self.pelanggan_ctrl = PanelMember(self.ui, self.show_custom_message)
        self.membership_ctrl = PanelMembership(self.ui, self.show_custom_message)
        self.transaksi_ctrl = TransaksiController(self.ui, self.membership_ctrl, self.pelanggan_ctrl)
        self.pelanggan_ctrl.set_membership_ctrl096(self.membership_ctrl)
        self.membership_ctrl.set_pelanggan_ctrl064(self.pelanggan_ctrl)

    def show_custom_message(self, title, message):
        CustomMessageBox.show_message(self.window, title, message)
    def go_to_landing(self):
        self.ui.stackedWidget.setCurrentIndex(0)
    def go_to_dashboard(self):
        self.ui.stackedWidget.setCurrentIndex(1)
    def go_to_membership(self):
        self.ui.stackedWidget.setCurrentIndex(2)
    def go_to_transaksi(self):
        self.transaksi_ctrl.buka_halaman_transaksi()
    def bukan_admin_exit(self):
        self.show_custom_message("ALERT!", "TERIMA KASIH ATAS KEJUJURANNYA!")
        sys.exit()
    def show(self):
        self.window.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    try:
        init_db()  # Buat tabel jika belum ada
    except Exception as e:
        QtWidgets.QMessageBox.critical(None, "Koneksi Database Gagal",
            f"Tidak dapat terhubung ke MySQL!\n\nPastikan MySQL berjalan dan database 'database_rentalps' sudah dibuat.\n\nError: {e}")
        sys.exit(1)
    app_instance = MainApp()
    app_instance.show()
    sys.exit(app.exec())
