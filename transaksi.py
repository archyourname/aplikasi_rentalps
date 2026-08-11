from PyQt6 import QtWidgets, QtCore

class TransaksiController:
    def __init__(self, ui, membership_ctrl, pelanggan_ctrl):
        self.ui = ui
        self.membership_ctrl = membership_ctrl
        self.pelanggan_ctrl = pelanggan_ctrl
        self.ui.tableTransaksi.setColumnCount(13)
        self.ui.tableTransaksi.setHorizontalHeaderLabels([
            'Pilih', 'Nama', 'Jaminan', 'WhatsApp', 'Alamat', 
            'Tgl Rental', 'Tgl Berakhir', 'Durasi', 
            'Tipe PS', 'Tier', 'Include TV', 'Antar (KM)', 'Total Biaya'
        ])
        self.ui.tableTransaksi.setColumnWidth(0, 50)
        self.ui.btnKembaliTransaksi.clicked.connect(self.kembali_ke_membership)
        self.ui.btnMaster064.clicked.connect(self.buka_halaman_transaksi)
        self.ui.btnEditPelangganDb.clicked.connect(self.edit_pelanggan_via_db)
        self.ui.btnEditMembershipDb.clicked.connect(self.edit_membership_via_db)
    def kembali_ke_membership(self):
        self.ui.stackedWidget.setCurrentIndex(2)    
    def buka_halaman_transaksi(self):
        self.refresh_table_database()
        self.ui.stackedWidget.setCurrentIndex(3)   
    def refresh_table_database(self):
        self.ui.tableTransaksi.setRowCount(0)
        pelanggan_list = self.pelanggan_ctrl.get_pelanggan_list096()
        for p in pelanggan_list:
            nama = p.get_nama096()
            jaminan = p.jaminan096
            wa = p.notlp096
            alamat = p.alamat096
            durasi = str(p.get_hari096())
            tgl_mulai = getattr(p, 'tgl_mulai096', '-')
            tgl_selesai = getattr(p, 'tgl_selesai096', '-')
            m_data = None
            for m in self.membership_ctrl.data_membership_list:
                if m['nama'] == nama:
                    m_data = m
                    break
            if m_data:
                tipe_ps = m_data['tipe_ps']
                tier = m_data['tier']
                include_tv = m_data['include_tv']
                antar_km = m_data['antar_km']
                total_biaya = m_data['total_biaya']
            else:
                tipe_ps = "Belum Transaksi"
                tier = "-"
                include_tv = "-"
                antar_km = "-"
                total_biaya = "-"
            row_position = self.ui.tableTransaksi.rowCount()
            self.ui.tableTransaksi.insertRow(row_position)
            chk_item = QtWidgets.QTableWidgetItem()
            chk_item.setFlags(QtCore.Qt.ItemFlag.ItemIsUserCheckable | QtCore.Qt.ItemFlag.ItemIsEnabled)
            chk_item.setCheckState(QtCore.Qt.CheckState.Unchecked)
            self.ui.tableTransaksi.setItem(row_position, 0, chk_item)
            self.ui.tableTransaksi.setItem(row_position, 1, QtWidgets.QTableWidgetItem(nama))
            self.ui.tableTransaksi.setItem(row_position, 2, QtWidgets.QTableWidgetItem(jaminan))
            self.ui.tableTransaksi.setItem(row_position, 3, QtWidgets.QTableWidgetItem(wa))
            self.ui.tableTransaksi.setItem(row_position, 4, QtWidgets.QTableWidgetItem(alamat))
            self.ui.tableTransaksi.setItem(row_position, 5, QtWidgets.QTableWidgetItem(tgl_mulai))
            self.ui.tableTransaksi.setItem(row_position, 6, QtWidgets.QTableWidgetItem(tgl_selesai))
            self.ui.tableTransaksi.setItem(row_position, 7, QtWidgets.QTableWidgetItem(durasi))
            self.ui.tableTransaksi.setItem(row_position, 8, QtWidgets.QTableWidgetItem(tipe_ps))
            self.ui.tableTransaksi.setItem(row_position, 9, QtWidgets.QTableWidgetItem(tier))
            self.ui.tableTransaksi.setItem(row_position, 10, QtWidgets.QTableWidgetItem(include_tv))
            self.ui.tableTransaksi.setItem(row_position, 11, QtWidgets.QTableWidgetItem(antar_km))
            self.ui.tableTransaksi.setItem(row_position, 12, QtWidgets.QTableWidgetItem(total_biaya))
    def _get_checked_row(self):
        for i in range(self.ui.tableTransaksi.rowCount()):
            item = self.ui.tableTransaksi.item(i, 0)
            if item and item.checkState() == QtCore.Qt.CheckState.Checked:
                return i
        return -1
    def edit_pelanggan_via_db(self):
        row = self._get_checked_row()
        if row == -1:
            self.membership_ctrl.show_message("PERINGATAN", "Pilih data yang ingin diedit!")
            return
        self.ui.stackedWidget.setCurrentIndex(1)
        for i in range(self.ui.tableWidget096.rowCount()):
            item = self.ui.tableWidget096.item(i, 0)
            if item:
                item.setCheckState(QtCore.Qt.CheckState.Checked if i == row else QtCore.Qt.CheckState.Unchecked)
        self.pelanggan_ctrl.edit_data096()
    def edit_membership_via_db(self):
        row = self._get_checked_row()
        if row == -1:
            self.membership_ctrl.show_message("PERINGATAN", "Pilih data yang ingin diedit!")
            return
        nama = self.ui.tableTransaksi.item(row, 1).text()
        self.ui.stackedWidget.setCurrentIndex(2)
        found = False
        for i in range(self.ui.tableMembership064.rowCount()):
            item = self.ui.tableMembership064.item(i, 0)
            if item:
                name_item = self.ui.tableMembership064.item(i, 1)
                if name_item and name_item.text() == nama:
                    item.setCheckState(QtCore.Qt.CheckState.Checked)
                    found = True
                else:
                    item.setCheckState(QtCore.Qt.CheckState.Unchecked)    
        if found:
            self.membership_ctrl.edit_membership064()
        else:
            self.membership_ctrl.show_message("PERINGATAN", f"Pelanggan '{nama}' belum memiliki data Membership/Transaksi untuk diedit!")
