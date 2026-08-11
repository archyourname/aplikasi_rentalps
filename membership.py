from PyQt6 import QtWidgets, QtCore
from koneksi_db import connect_db


class PanelMembership:
    def __init__(self, ui, show_message_callback):
        self.__init__064(ui, show_message_callback)

    def __init__064(self, ui, show_message_callback):
        self.ui = ui
        self.show_message = show_message_callback
        self.data_membership_list = []
        self.pelanggan_ctrl = None
        self.ui.tableMembership064.setColumnCount(7)
        self.ui.tableMembership064.setHorizontalHeaderLabels(
            ['Pilih', 'Nama Pelanggan', 'Tier/Diskon', 'Tipe PS', 'Include TV', 'Antar (KM)', 'Total Biaya']
        )
        self.ui.tableMembership064.setColumnWidth(0, 50)
        self.ui.memberGabung064.setDate(QtCore.QDate.currentDate())
        self.ui.simpanMember064.clicked.connect(self.simpan_membership)
        self.ui.editMember064.clicked.connect(self.edit_membership064)
        self.ui.hpsMember064.clicked.connect(self.hapus_membership064)
        self.load_from_db064()

    # ═══════════════════════════════════════════════════════════════
    #  MySQL helpers
    # ═══════════════════════════════════════════════════════════════

    def load_from_db064(self):
        """Muat hanya baris yang sudah punya data membership (Tipe PS tidak kosong)."""
        self.data_membership_list = []
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT Nama, `Tipe PS`, Tier, `Include TV`, Jarak, `Total Biaya`, "
                "`Tanggal Rental` "
                "FROM membership "
                "ORDER BY id ASC"
            )
            rows = cursor.fetchall()
            cursor.close()
            conn.close()

            tipe_map = {'PS2': 0, 'PS3': 1, 'PS4': 2, 'PS5': 3}
            for row in rows:
                nama       = row[0] or ''
                tipe_ps    = row[1] or ''
                tier       = row[2] or 'No Member - 0%'
                include_tv = row[3] or 'Tidak'
                jarak      = int(row[4]) if row[4] else 0
                total      = row[5] or ''
                tgl        = row[6] or ''

                tipe_ps_idx = 0
                for key, idx in tipe_map.items():
                    if key in tipe_ps:
                        tipe_ps_idx = idx
                        break

                self.data_membership_list.append({
                    'nama'           : nama,
                    'tier'           : tier,
                    'tipe_ps'        : tipe_ps,
                    'tipe_ps_idx'    : tipe_ps_idx,
                    'include_tv_bool': include_tv == 'Ya',
                    'include_tv'     : include_tv,
                    'antar_bool'     : jarak > 0,
                    'jarak_val'      : jarak,
                    'antar_km'       : f"{jarak} KM" if jarak > 0 else '-',
                    'total_biaya'    : total,
                    'tgl'            : tgl
                })
        except Exception as e:
            self.show_message("ERROR DB", f"Gagal memuat data membership:\n{e}")
        self.refresh_table_membership064()

    def _db_update_membership064(self, member_data):
        """UPDATE kolom-kolom membership pada baris yang sudah ada."""
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO membership "
                "(Nama, `Tipe PS`, Tier, `Include TV`, Jarak, `Total Biaya`, `Tanggal Rental`) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s) "
                "ON DUPLICATE KEY UPDATE "
                "`Tipe PS`=VALUES(`Tipe PS`), Tier=VALUES(Tier), "
                "`Include TV`=VALUES(`Include TV`), Jarak=VALUES(Jarak), "
                "`Total Biaya`=VALUES(`Total Biaya`), `Tanggal Rental`=VALUES(`Tanggal Rental`)",
                (
                    member_data['nama'],
                    member_data['tipe_ps'],
                    member_data['tier'],
                    member_data['include_tv'],
                    member_data['jarak_val'],
                    member_data['total_biaya'],
                    member_data['tgl']
                )
            )
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            self.show_message("ERROR DB", f"Gagal simpan membership ke database:\n{e}")

    def _db_clear_membership064(self, nama):
        """Kosongkan kolom membership (biarkan baris pelanggan tetap ada)."""
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM membership WHERE Nama = %s",
                (nama,)
            )
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            self.show_message("ERROR DB", f"Gagal hapus membership dari database:\n{e}")

    # ═══════════════════════════════════════════════════════════════
    #  UI Methods
    # ═══════════════════════════════════════════════════════════════

    def set_pelanggan_ctrl064(self, ctrl):
        self.pelanggan_ctrl = ctrl
        self.refresh_combo_pelanggan064()

    def refresh_combo_pelanggan064(self):
        self.ui.opsiPelanggan064.clear()
        if self.pelanggan_ctrl:
            pelanggan_list = self.pelanggan_ctrl.get_pelanggan_list096()
            self.ui.opsiPelanggan064.addItems([p.get_nama096() for p in pelanggan_list])

    def refresh_table_membership064(self):
        self.ui.tableMembership064.setRowCount(0)
        for m in self.data_membership_list:
            row_position = self.ui.tableMembership064.rowCount()
            self.ui.tableMembership064.insertRow(row_position)
            chk_item = QtWidgets.QTableWidgetItem()
            chk_item.setFlags(
                QtCore.Qt.ItemFlag.ItemIsUserCheckable | QtCore.Qt.ItemFlag.ItemIsEnabled
            )
            chk_item.setCheckState(QtCore.Qt.CheckState.Unchecked)
            self.ui.tableMembership064.setItem(row_position, 0, chk_item)
            self.ui.tableMembership064.setItem(row_position, 1, QtWidgets.QTableWidgetItem(m['nama']))
            self.ui.tableMembership064.setItem(row_position, 2, QtWidgets.QTableWidgetItem(m['tier']))
            self.ui.tableMembership064.setItem(row_position, 3, QtWidgets.QTableWidgetItem(m['tipe_ps']))
            self.ui.tableMembership064.setItem(row_position, 4, QtWidgets.QTableWidgetItem(m['include_tv']))
            self.ui.tableMembership064.setItem(row_position, 5, QtWidgets.QTableWidgetItem(m['antar_km']))
            self.ui.tableMembership064.setItem(row_position, 6, QtWidgets.QTableWidgetItem(m['total_biaya']))

    def simpan_membership(self):
        nama = self.ui.opsiPelanggan064.currentText()
        if not nama:
            self.show_message("PERINGATAN", "Tidak ada pelanggan! Silakan tambah Data Pelanggan terlebih dahulu.")
            return

        tipe_ps_idx  = self.ui.opsiTipePS064.currentIndex()
        tipe_ps_text = self.ui.opsiTipePS064.currentText()
        include_tv   = self.ui.cekTV064.isChecked()
        antar        = self.ui.kurir064.isChecked()
        jarak_km     = self.ui.jarak064.value()
        tier         = self.ui.opsiTier064.currentText()
        tgl          = self.ui.memberGabung064.date().toString("dd/MM/yyyy")

        durasi = 1
        if self.pelanggan_ctrl:
            for p in self.pelanggan_ctrl.get_pelanggan_list096():
                if p.get_nama096() == nama:
                    durasi = p.get_hari096()
                    break

        base_price    = [10000, 20000, 30000, 40000][tipe_ps_idx]
        tv_price      = 15000 if include_tv else 0
        discount_pct  = 0.0
        if "10%" in tier:   discount_pct = 0.1
        elif "20%" in tier: discount_pct = 0.2
        elif "30%" in tier: discount_pct = 0.3
        elif "40%" in tier: discount_pct = 0.4
        subtotal        = (base_price + tv_price) * durasi
        discount_amount = subtotal * discount_pct
        ongkir          = 2500 * jarak_km if antar else 0
        total           = int(subtotal - discount_amount + ongkir)
        total_str       = f"Rp {total:,}"

        member_data = {
            'nama'           : nama,
            'tier'           : tier,
            'tipe_ps'        : tipe_ps_text,
            'tipe_ps_idx'    : tipe_ps_idx,
            'include_tv_bool': include_tv,
            'include_tv'     : "Ya" if include_tv else "Tidak",
            'antar_bool'     : antar,
            'jarak_val'      : jarak_km,
            'antar_km'       : f"{jarak_km} KM" if antar else "-",
            'total_biaya'    : total_str,
            'tgl'            : tgl
        }

        # Update list lokal
        found = False
        for i, m in enumerate(self.data_membership_list):
            if m['nama'] == nama:
                self.data_membership_list[i] = member_data
                found = True
                break
        if not found:
            self.data_membership_list.append(member_data)

        # UPDATE ke MySQL
        self._db_update_membership064(member_data)
        self.refresh_table_membership064()
        self.ui.opsiTipePS064.setCurrentIndex(0)
        self.ui.opsiTier064.setCurrentIndex(0)
        self.ui.cekTV064.setChecked(False)
        self.ui.kurir064.setChecked(False)
        self.ui.jarak064.setValue(0)
        self.ui.memberGabung064.setDate(QtCore.QDate.currentDate())
        self.show_message("SUKSES", f"Transaksi '{nama}' berhasil disimpan!")

    def edit_membership064(self):
        rows_to_edit = [
            i for i in range(self.ui.tableMembership064.rowCount())
            if self.ui.tableMembership064.item(i, 0) and
               self.ui.tableMembership064.item(i, 0).checkState() == QtCore.Qt.CheckState.Checked
        ]
        if len(rows_to_edit) == 0:
            self.show_message("PERINGATAN", "Silakan centang satu data membership untuk diedit!")
            return
        if len(rows_to_edit) > 1:
            self.show_message("PERINGATAN", "Hanya dapat mengedit satu membership pada satu waktu!")
            return

        selected_row = rows_to_edit[0]
        member = self.data_membership_list[selected_row]

        idx_pelanggan = self.ui.opsiPelanggan064.findText(member['nama'])
        if idx_pelanggan >= 0:
            self.ui.opsiPelanggan064.setCurrentIndex(idx_pelanggan)
        self.ui.opsiTipePS064.setCurrentIndex(member['tipe_ps_idx'])
        self.ui.opsiTier064.setCurrentText(member['tier'])
        self.ui.cekTV064.setChecked(member['include_tv_bool'])
        self.ui.kurir064.setChecked(member['antar_bool'])
        self.ui.jarak064.setValue(member['jarak_val'])
        qdate = QtCore.QDate.fromString(member['tgl'], "dd/MM/yyyy")
        if qdate.isValid():
            self.ui.memberGabung064.setDate(qdate)

        self.show_message("INFO", "Data dipindahkan ke formulir. Ubah dan klik SIMPAN.")

    def hapus_membership064(self):
        rows_to_delete = [
            i for i in range(self.ui.tableMembership064.rowCount())
            if self.ui.tableMembership064.item(i, 0) and
               self.ui.tableMembership064.item(i, 0).checkState() == QtCore.Qt.CheckState.Checked
        ]
        if not rows_to_delete:
            self.show_message("PERINGATAN", "Pilih data membership untuk dihapus!")
            return
        for i in reversed(rows_to_delete):
            nama_dihapus = self.data_membership_list[i]['nama']
            self.data_membership_list.pop(i)
            self._db_clear_membership064(nama_dihapus)
        self.refresh_table_membership064()
        self.show_message("SUKSES", f"{len(rows_to_delete)} data membership berhasil dihapus!")

    def add_or_update_member064(self, nama, tier):
        for m in self.data_membership_list:
            if m['nama'] == nama:
                m['tier'] = tier
                self.refresh_table_membership064()
                return
        self.data_membership_list.append({
            'nama'           : nama,
            'tier'           : tier,
            'tipe_ps'        : 'PS2 (Rp 10.000/hari)',
            'tipe_ps_idx'    : 0,
            'include_tv_bool': False,
            'include_tv'     : 'Tidak',
            'antar_bool'     : False,
            'jarak_val'      : 0,
            'antar_km'       : '-',
            'total_biaya'    : 'Rp 0',
            'tgl'            : QtCore.QDate.currentDate().toString("dd/MM/yyyy")
        })
        self.refresh_table_membership064()

    def remove_member_by_name064(self, nama):
        self.data_membership_list = [m for m in self.data_membership_list if m['nama'] != nama]
        self.refresh_table_membership064()
