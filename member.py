from PyQt6 import QtWidgets, QtCore
from koneksi_db import connect_db


class DataPelanggan:
    def __init__(self, nama, alamat, jaminan, tgl_mulai, tgl_selesai, durasi, notlp):
        self.__init__096(nama, alamat, jaminan, tgl_mulai, tgl_selesai, durasi, notlp)

    def __init__096(self, nama, alamat, jaminan, tgl_mulai, tgl_selesai, durasi, notlp):
        self.nama096 = nama
        self.alamat096 = alamat
        self.jaminan096 = jaminan
        self.tgl_mulai096 = tgl_mulai
        self.tgl_selesai096 = tgl_selesai
        self.__durasi096 = durasi
        self.notlp096 = notlp

    def get_nama096(self):
        return self.nama096

    def set_nama096(self, nama_baru096):
        self.nama096 = nama_baru096

    def get_hari096(self):
        return self.__durasi096

    def tampilkan096(self):
        print("\n=== DATA PELANGGAN JAWARAPS ===")
        print("Nama        :", self.nama096)
        print("Alamat      :", self.alamat096)
        print("Jaminan     :", self.jaminan096)
        print("Mulai       :", self.tgl_mulai096)
        print("Selesai     :", self.tgl_selesai096)
        print("No Telepon  :", self.notlp096)
        print("Durasi      :", self.__durasi096, "HARI")

    def hitung_biaya096(self):
        return 0


class PanelMember:
    def __init__(self, ui, show_message_callback):
        self.__init__096(ui, show_message_callback)

    def __init__096(self, ui, show_message_callback):
        self.ui = ui
        self.show_message = show_message_callback
        self.data_pelanggan_list = []
        self.membership_ctrl = None
        self._edit_old_nama = None          
        self.ui.tableWidget096.setColumnCount(8)
        self.ui.tableWidget096.setHorizontalHeaderLabels(
            ['Pilih', 'Nama', 'Jaminan', 'Tgl Mulai', 'Tgl Berakhir', 'Durasi', 'WhatsApp', 'Alamat']
        )
        self.ui.tableWidget096.setColumnWidth(0, 50)
        self.ui.dateMulai096.setDate(QtCore.QDate.currentDate())
        self.ui.dateSelesai096.setDate(QtCore.QDate.currentDate().addDays(1))
        self.ui.btnSimpan096.clicked.connect(self.simpan_data096)
        self.ui.btnEdit096.clicked.connect(self.edit_data096)
        self.ui.btnDelete096.clicked.connect(self.hapus_data096)
        self.load_from_db096()

    def load_from_db096(self):
        self.data_pelanggan_list = []
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT Nama, Jaminan, WhatsApp, Alamat, "
                "`Tanggal Rental`, `Tanggal Berakhir`, Durasi "
                "FROM member ORDER BY id ASC"
            )
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            seen = set()
            for row in rows:
                nama = row[0]
                if nama and nama not in seen:
                    seen.add(nama)
                    self.data_pelanggan_list.append(
                        DataPelanggan(
                            nama=row[0],
                            jaminan=row[1] or '',
                            notlp=row[2] or '',
                            alamat=row[3] or '',
                            tgl_mulai=row[4] or '',
                            tgl_selesai=row[5] or '',
                            durasi=row[6] or 0
                        )
                    )
        except Exception as e:
            self.show_message("ERROR DB", f"Gagal memuat data pelanggan:\n{e}")
        self.update_table_ui096()

    def _db_nama_exists096(self, nama):
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM member WHERE Nama = %s LIMIT 1", (nama,))
            row = cursor.fetchone()
            cursor.close()
            conn.close()
            return row is not None
        except Exception as e:
            self.show_message("ERROR DB", f"Gagal cek data:\n{e}")
            return False

    def _db_insert(self, p):
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO member "
                "(Nama, Jaminan, WhatsApp, Alamat, "
                "`Tanggal Rental`, `Tanggal Berakhir`, Durasi) "
                "VALUES (%s,%s,%s,%s,%s,%s,%s)",
                (
                    p.get_nama096(), p.jaminan096, p.notlp096, p.alamat096,
                    p.tgl_mulai096, p.tgl_selesai096, p.get_hari096()
                )
            )
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            self.show_message("ERROR DB", f"Gagal INSERT data:\n{e}")

    def _db_update096(self, p, old_nama=None):
        target_nama = old_nama if old_nama else p.get_nama096()
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE member SET "
                "Nama = %s, "
                "Jaminan = %s, "
                "WhatsApp = %s, "
                "Alamat = %s, "
                "`Tanggal Rental` = %s, "
                "`Tanggal Berakhir` = %s, "
                "Durasi = %s "
                "WHERE Nama = %s",
                (
                    p.get_nama096(), p.jaminan096, p.notlp096, p.alamat096,
                    p.tgl_mulai096, p.tgl_selesai096, p.get_hari096(),
                    target_nama
                )
            )
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            self.show_message("ERROR DB", f"Gagal UPDATE data:\n{e}")

    def _db_delete096(self, nama):
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM member WHERE Nama = %s", (nama,))
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            self.show_message("ERROR DB", f"Gagal DELETE data:\n{e}")

    # ═══════════════════════════════════════════════════════════════
    #  UI Methods
    # ═══════════════════════════════════════════════════════════════

    def set_membership_ctrl096(self, ctrl):
        self.membership_ctrl = ctrl
        if self.membership_ctrl:
            self.membership_ctrl.refresh_combo_pelanggan064()

    def update_table_ui096(self):
        self.ui.tableWidget096.setRowCount(0)
        for pelanggan in self.data_pelanggan_list:
            row_position = self.ui.tableWidget096.rowCount()
            self.ui.tableWidget096.insertRow(row_position)
            chk_item = QtWidgets.QTableWidgetItem()
            chk_item.setFlags(
                QtCore.Qt.ItemFlag.ItemIsUserCheckable | QtCore.Qt.ItemFlag.ItemIsEnabled
            )
            chk_item.setCheckState(QtCore.Qt.CheckState.Unchecked)
            self.ui.tableWidget096.setItem(row_position, 0, chk_item)
            self.ui.tableWidget096.setItem(row_position, 1, QtWidgets.QTableWidgetItem(pelanggan.get_nama096()))
            self.ui.tableWidget096.setItem(row_position, 2, QtWidgets.QTableWidgetItem(pelanggan.jaminan096))
            self.ui.tableWidget096.setItem(row_position, 3, QtWidgets.QTableWidgetItem(pelanggan.tgl_mulai096))
            self.ui.tableWidget096.setItem(row_position, 4, QtWidgets.QTableWidgetItem(pelanggan.tgl_selesai096))
            self.ui.tableWidget096.setItem(row_position, 5, QtWidgets.QTableWidgetItem(f"{pelanggan.get_hari096()} Hari"))
            self.ui.tableWidget096.setItem(row_position, 6, QtWidgets.QTableWidgetItem(pelanggan.notlp096))
            self.ui.tableWidget096.setItem(row_position, 7, QtWidgets.QTableWidgetItem(pelanggan.alamat096))

    def simpan_data096(self):
        nama      = self.ui.editNama096.text().strip()
        jaminan   = self.ui.editJaminan096.text().strip()
        wa        = self.ui.editWa096.text().strip()
        alamat    = self.ui.textAlamat096.toPlainText().strip()
        date_mulai   = self.ui.dateMulai096.date()
        date_selesai = self.ui.dateSelesai096.date()
        durasi = date_mulai.daysTo(date_selesai)

        if not nama or not jaminan or not wa or not alamat:
            self.show_message("PERINGATAN", "Semua data formulir harus diisi!")
            return
        if durasi < 0:
            self.show_message("PERINGATAN", "Tanggal Berakhir tidak boleh lebih awal dari Tanggal Rental!")
            return

        tgl_mulai_str   = date_mulai.toString("dd/MM/yyyy")
        tgl_selesai_str = date_selesai.toString("dd/MM/yyyy")
        pelanggan = DataPelanggan(nama, alamat, jaminan, tgl_mulai_str, tgl_selesai_str, durasi, wa)

        old_nama = self._edit_old_nama          

        if old_nama:
            self._db_update096(pelanggan, old_nama=old_nama)

            for i, p in enumerate(self.data_pelanggan_list):
                if p.get_nama096() == old_nama:
                    self.data_pelanggan_list[i] = pelanggan
                    break

            if old_nama != nama and self.membership_ctrl:
                for m in self.membership_ctrl.data_membership_list:
                    if m['nama'] == old_nama:
                        m['nama'] = nama
                self.membership_ctrl.refresh_table_membership064()

            self._edit_old_nama = None
        else:
            if self._db_nama_exists096(nama):
                self.show_message("PERINGATAN", f"Nama '{nama}' sudah ada di database!")
                return
            self._db_insert(pelanggan)
            self.data_pelanggan_list.append(pelanggan)

        self.update_table_ui096()
        self.ui.editNama096.clear()
        self.ui.editJaminan096.clear()
        self.ui.editWa096.clear()
        self.ui.textAlamat096.clear()
        self.ui.dateMulai096.setDate(QtCore.QDate.currentDate())
        self.ui.dateSelesai096.setDate(QtCore.QDate.currentDate().addDays(1))
        if self.membership_ctrl:
            self.membership_ctrl.refresh_combo_pelanggan064()
        self.show_message("SUKSES", f"Data atas nama '{nama}' berhasil disimpan!")

    def edit_data096(self):
        rows_to_edit = [
            i for i in range(self.ui.tableWidget096.rowCount())
            if self.ui.tableWidget096.item(i, 0) and
               self.ui.tableWidget096.item(i, 0).checkState() == QtCore.Qt.CheckState.Checked
        ]
        if len(rows_to_edit) == 0:
            self.show_message("PERINGATAN", "Silakan centang satu data di tabel untuk diedit!")
            return
        if len(rows_to_edit) > 1:
            self.show_message("PERINGATAN", "Hanya dapat mengedit satu data pada satu waktu!")
            return

        selected_row = rows_to_edit[0]
        pelanggan = self.data_pelanggan_list[selected_row]

        self.ui.editNama096.setText(pelanggan.get_nama096())
        self.ui.editJaminan096.setText(pelanggan.jaminan096)
        self.ui.editWa096.setText(pelanggan.notlp096)
        self.ui.textAlamat096.setPlainText(pelanggan.alamat096)
        qdate_mulai = QtCore.QDate.fromString(pelanggan.tgl_mulai096, "dd/MM/yyyy")
        if qdate_mulai.isValid():
            self.ui.dateMulai096.setDate(qdate_mulai)
        qdate_selesai = QtCore.QDate.fromString(pelanggan.tgl_selesai096, "dd/MM/yyyy")
        if qdate_selesai.isValid():
            self.ui.dateSelesai096.setDate(qdate_selesai)

        self._edit_old_nama = pelanggan.get_nama096()

        if self.membership_ctrl:
            self.membership_ctrl.refresh_combo_pelanggan064()
        self.show_message("INFO", "Data dipindahkan ke formulir. Silakan ubah data dan klik SIMPAN.")

    def hapus_data096(self):
        rows_to_delete = [
            i for i in range(self.ui.tableWidget096.rowCount())
            if self.ui.tableWidget096.item(i, 0) and
               self.ui.tableWidget096.item(i, 0).checkState() == QtCore.Qt.CheckState.Checked
        ]
        if not rows_to_delete:
            self.show_message("PERINGATAN", "Silakan centang data yang ingin dihapus!")
            return
        for i in reversed(rows_to_delete):
            if i < len(self.data_pelanggan_list):
                nama_hapus = self.data_pelanggan_list[i].get_nama096()
                self._db_delete096(nama_hapus)
                self.data_pelanggan_list.pop(i)
                if self.membership_ctrl:
                    self.membership_ctrl.remove_member_by_name064(nama_hapus)
        self.update_table_ui096()
        if self.membership_ctrl:
            self.membership_ctrl.refresh_combo_pelanggan064()
        self.show_message("SUKSES", f"{len(rows_to_delete)} data berhasil dihapus!")

    def get_pelanggan_list096(self):
        return self.data_pelanggan_list
