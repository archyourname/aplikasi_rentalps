# /=================================================================\
# ||                                                                ||
# ||=============          APLIKASI RENTALPS          ============= ||
# ||                                                                ||
# \=================================================================/
# Aplikasi rentalps by RAFFY VIBTO RAMADHAN & NESA KUSUMA BARATA

*Aplikasi ini dibuat untuk melengkapi tugas Pertemuan 9 Fundamental Pemprograman Object - RAFFY VIBTO RAMADHAN(2514010064), NESA KUSUMA BARATA(2514010096)* 

Terima kasih kepada Pak Robi Wariyanto Abdullah,M.Kom selaku dosen mengampu mata kuliah Fundamental Pemprograman Object, karena telah memberikan pengetahuan sehingga aplikasi terus bisa berinovasi



# THIS REFERENCE DESIGN
  *https://toonrobotics.com/en/pyside_app_making_part1en/*

## Perintah Penting!!
- *Konverter (QT-Designer › Python)*
        (python -m PyQt6.uic.pyuic -x rental.ui -o rental.py)
- *PyInstaller → Konverter (Python › .exe)*
         CMD → (pip install pyinstaller) → (python -m PyInstaller --onefile rentalps.py)

## BUGS AND UPDATE
- [BUGS] 
    ➔ Data Membership tidak bisa dibuka karena conflict dengan data pelanggan [SOLVED] 
    ➔ Tombol dan tampilan kurang sesuai, untuk tombol "bukan admin" [SOLVED] 
    ➔ Terjadi error atau gagal saat data pelanggan baru disimpan [SOLVED] 
    ➔ pada form "Jenis Member" kurang efisien [SOLVED] 
    ➔ Terdapat "Nomor Kartu" tidak berguna [SOLVED]
    ➔ Error saat pemanggilan Atribut ketika menampilkan riwayat transaksi pelanggan [SOLVED]
- [UPDATE_V.1]
    [1] Memisahkan file menjadi rental.py, member.py, dan membership.py, lalu disatukan dalam file utama rentalps.py
    [2] Menambahkan tombol peringatan di bawah tombol utama yang menampilkan pesan "Terima kasih atas kejujurannya" lalu keluar program otomatis.
    [3] Memperbaiki logika CRUD (Create, Read, Update, Delete) di seluruh file Python agar data tersimpan dan terbaca dengan benar ke dalam sistem
    [4] Mengubah "Jenis Member" menjadi Dropdown "Tanggal Rental" dan "Durasi"
    [5] Mengganti "Nomor Kartu" menjadi Dropdown Tipe PS, Menambahkan Checkbox "Include TV" dan opsi "Jarak Pengantaran (KM)"
    [6] Memperbaiki Getter pada kode

- [BUGS]
    ➔ Data Pelanggan dan Data Membership terpisah [SOLVED]
- [UPDATE_V.2]
    [1] Membuat halaman Database Pelanggan Master berisi 13 kolom yang menggabungkan data dari member.py dan membership.py

- [UPDATE_V.3]
    [1] Mengubah objectname pada rental.ui menjadi 3 digit nim
    [2] Mengubah setiap function pada member.py dan membership.py pada setiap function
    [3] Menambahkan Data Dummy sebanyak 2, total menjadi 5 Data Dummy
    
- [UPDATE_V.4]
    [1] Penghapusan kelas Inheritance dan Multiple Inheritance pada member.py dan membership.py


## TEST CRUD PYTHON [OPSIONAL]
import sys
import unittest
from PyQt6 import QtWidgets, QtCore
from rental import Ui_MainWindow
from member import PanelMember
from membership import PanelMembership
app = QtWidgets.QApplication(sys.argv)

class DummyMainApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.messages = []
        def show_custom_message(title, message):
            self.messages.append((title, message))
        self.pelanggan_ctrl = PanelMember(self.ui, show_custom_message)
        self.membership_ctrl = PanelMembership(self.ui, show_custom_message)
        self.pelanggan_ctrl.set_membership_ctrl096(self.membership_ctrl)
        self.membership_ctrl.set_pelanggan_ctrl064(self.pelanggan_ctrl)

class TestCRUD(unittest.TestCase):
    def setUp(self):
        self.main_app = DummyMainApp()
        self.pelanggan_ctrl = self.main_app.pelanggan_ctrl
        self.membership_ctrl = self.main_app.membership_ctrl
        self.ui = self.main_app.ui
    def test_1_create_pelanggan(self):
        initial_count = len(self.pelanggan_ctrl.get_pelanggan_list096())
        self.ui.editNama096.setText("TestUser")
        self.ui.editJaminan096.setText("KTP")
        self.ui.editWa096.setText("08123456")
        self.ui.textAlamat096.setPlainText("Jl. Testing")
        self.pelanggan_ctrl.simpan_data096()
        new_count = len(self.pelanggan_ctrl.get_pelanggan_list096())
        self.assertEqual(new_count, initial_count + 1, "Data Pelanggan gagal ditambah")
        self.assertEqual(self.pelanggan_ctrl.get_pelanggan_list096()[-1].get_nama096(), "TestUser")

    def test_2_edit_pelanggan(self):
        self.ui.editNama096.setText("EditUser")
        self.ui.editJaminan096.setText("SIM")
        self.ui.editWa096.setText("081111")
        self.ui.textAlamat096.setPlainText("Jl. Edit")
        self.pelanggan_ctrl.simpan_data096()
        row_count = self.ui.tableWidget096.rowCount()
        self.ui.tableWidget096.item(row_count - 1, 0).setCheckState(QtCore.Qt.CheckState.Checked)
        self.pelanggan_ctrl.edit_data096()
        self.ui.editNama096.setText("EditUserBerubah")
        self.pelanggan_ctrl.simpan_data096()
        self.assertEqual(self.pelanggan_ctrl.get_pelanggan_list096()[-1].get_nama096(), "EditUserBerubah")
    def test_3_hapus_pelanggan(self):
        self.ui.editNama096.setText("DeleteUser")
        self.ui.editJaminan096.setText("BPJS")
        self.ui.editWa096.setText("081111")
        self.ui.textAlamat096.setPlainText("Jl. Delete")
        self.pelanggan_ctrl.simpan_data096()
        initial_count = len(self.pelanggan_ctrl.get_pelanggan_list096())
        row_count = self.ui.tableWidget096.rowCount()
        self.ui.tableWidget096.item(row_count - 1, 0).setCheckState(QtCore.Qt.CheckState.Checked)
        self.pelanggan_ctrl.hapus_data096()
        new_count = len(self.pelanggan_ctrl.get_pelanggan_list096())
        self.assertEqual(new_count, initial_count - 1, "Data gagal dihapus")
    def test_4_create_membership(self):
        initial_count = len(self.membership_ctrl.data_membership_list)
        
        self.ui.opsiPelanggan064.setCurrentIndex(0)
        self.ui.opsiTipePS064.setCurrentIndex(1)
        self.ui.opsiTier064.setCurrentIndex(1)
        self.ui.cekTV064.setChecked(True)
        self.ui.kurir064.setChecked(False)
        self.ui.jarak064.setValue(0)
        self.membership_ctrl.simpan_membership064()
        
        new_count = len(self.membership_ctrl.data_membership_list)
        for m in self.membership_ctrl.data_membership_list:
            if m['nama'] == 'Kuyhaa':
                self.assertEqual(m['tipe_ps_idx'], 1)
                self.assertEqual(m['include_tv_bool'], True)
    def test_5_hapus_membership(self):
        initial_count = len(self.membership_ctrl.data_membership_list)
        self.ui.tableMembership064.item(0, 0).setCheckState(QtCore.Qt.CheckState.Checked)
        self.membership_ctrl.hapus_membership064()
        new_count = len(self.membership_ctrl.data_membership_list)
        self.assertEqual(new_count, initial_count - 1)
if __name__ == '__main__':
    print("=== MENJALANKAN PENGUJIAN (TEST) CRUD ===")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCRUD)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
    print("\nPengujian selesai!")
    import os
    os.system('pause')

## JALANKAN SQL [OPSIONAL]
python -c "import pymysql; conn=pymysql.connect(host='localhost', user='root', password=''); cursor=conn.cursor(); cursor.execute('DROP DATABASE IF EXISTS UAS_RentalPS'); conn.commit(); cursor.close(); conn.close()"
python koneksi_db.py