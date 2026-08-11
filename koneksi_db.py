import pymysql


def connect_db():
    try:
        return pymysql.connect(
            host="localhost",
            user="root",
            password="",
            database="RentalPS",
            cursorclass=pymysql.cursors.Cursor
        )
    except pymysql.err.OperationalError as e:
        if e.args[0] == 1049:
            conn = pymysql.connect(
                host="localhost",
                user="root",
                password="",
            )
            with conn.cursor() as cursor:
                cursor.execute("CREATE DATABASE RentalPS")
            conn.commit()
            conn.close()
            return pymysql.connect(
                host="localhost",
                user="root",
                password="",
                database="RentalPS",
                cursorclass=pymysql.cursors.Cursor
            )
        else:
            raise


def init_db():
    """Buat tabel member dan membership jika belum ada."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS member ("
        "id INT AUTO_INCREMENT PRIMARY KEY, "
        "Nama VARCHAR(255) NOT NULL UNIQUE, "
        "Jaminan VARCHAR(100), "
        "WhatsApp VARCHAR(20), "
        "Alamat TEXT, "
        "`Tanggal Rental` VARCHAR(20), "
        "`Tanggal Berakhir` VARCHAR(20), "
        "Durasi INT"
        ")"
    )
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS membership ("
        "id INT AUTO_INCREMENT PRIMARY KEY, "
        "Nama VARCHAR(255) NOT NULL UNIQUE, "
        "`Tipe PS` VARCHAR(50), "
        "Tier VARCHAR(50), "
        "`Include TV` VARCHAR(20), "
        "Jarak INT, "
        "`Total Biaya` VARCHAR(50), "
        "`Tanggal Rental` VARCHAR(20), "
        "FOREIGN KEY (Nama) REFERENCES member(Nama) ON DELETE CASCADE ON UPDATE CASCADE"
        ")"
    )
    
    cursor.execute("SELECT COUNT(*) FROM member")
    jumlah = cursor.fetchone()[0]
    if jumlah == 0:
        cursor.execute("""
            INSERT INTO member 
            (Nama, Jaminan, WhatsApp, Alamat, `Tanggal Rental`, `Tanggal Berakhir`, Durasi)
            VALUES 
            ('Kuyhaa', 'Ijazah', '081234567890', 'Jl. Ratapan Solo', '23/06/2026', '24/06/2026', 1),
            ('Bagas31', 'Kartu BPJS', '081298765432', 'Jl. Gorong Gorong Jock Owie', '23/06/2026', '24/06/2026', 1),
            ('DODI Repack', 'KTM', '081211223344', 'Jl. EM BEG', '23/06/2026', '24/06/2026', 1),
            ('Giga Purbalingga', 'KTP', '081122334455', 'Jl. Sudirman', '23/06/2026', '25/06/2026', 2),
            ('Skidrow', 'SIM', '089988776655', 'Jl. Thamrin', '23/06/2026', '26/06/2026', 3)
        """)
        cursor.execute("""
            INSERT INTO membership 
            (Nama, `Tipe PS`, Tier, `Include TV`, Jarak, `Total Biaya`, `Tanggal Rental`)
            VALUES 
            ('Kuyhaa', 'PS2 (Rp 10.000/hari)', 'Bronze - 10%', 'Tidak', 0, 'Rp 10,000', '23/06/2026'),
            ('Bagas31', 'PS3 (Rp 20.000/hari)', 'Silver - 20%', 'Ya', 0, 'Rp 28,000', '23/06/2026'),
            ('DODI Repack', 'PS4 (Rp 30.000/hari)', 'No Member - 0%', 'Tidak', 2, 'Rp 35,000', '23/06/2026'),
            ('Giga Purbalingga', 'PS2 (Rp 10.000/hari)', 'Silver - 20%', 'Ya', 2, 'Rp 35,000', '23/06/2026'),
            ('Skidrow', 'PS2 (Rp 10.000/hari)', 'Bronze - 10%', 'Tidak', 0, 'Rp 18,000', '23/06/2026')
        """)
        print("Data dummy otomatis ditambahkan!")
        
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    print("Mengecek dan membuat database beserta tabel jika belum ada...")
    init_db()
    print("Database 'RentalPS' dan tabel 'member' & 'membership' siap digunakan!")