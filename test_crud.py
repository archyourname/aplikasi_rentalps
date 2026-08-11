from member import PanelMember
from membership import PanelMembership

class MockUI:
    class Table:
        def setColumnCount(self, c): pass
        def setHorizontalHeaderLabels(self, l): pass
        def setColumnWidth(self, c, w): pass
        def setRowCount(self, c): pass
        def rowCount(self): return 0
        def insertRow(self, r): pass
        def setItem(self, r, c, i): pass
    
    class Date:
        def setDate(self, d): pass
        def date(self): return None

    class Btn:
        def __init__(self):
            self.clicked = type('sig', (), {'connect': lambda *args, **kwargs: None})()

    def __init__(self):
        self.tableWidget096 = self.Table()
        self.tableMembership064 = self.Table()
        self.dateMulai096 = self.Date()
        self.dateSelesai096 = self.Date()
        self.memberGabung064 = self.Date()
        self.btnSimpan096 = self.Btn()
        self.btnEdit096 = self.Btn()
        self.btnDelete096 = self.Btn()
        self.simpanMember064 = self.Btn()
        self.editMember064 = self.Btn()
        self.hpsMember064 = self.Btn()

def show_msg(*args):
    print("MSG:", args)

ui = MockUI()
print("Testing PanelMember...")
pm = PanelMember(ui, show_msg)
print(f"Loaded {len(pm.data_pelanggan_list)} members.")
for p in pm.data_pelanggan_list:
    print(" -", p.get_nama096())

print("\nTesting PanelMembership...")
pmemb = PanelMembership(ui, show_msg)
print(f"Loaded {len(pmemb.data_membership_list)} memberships.")
for m in pmemb.data_membership_list:
    print(" -", m['nama'], m['tipe_ps'])

print("\nAll Good!")
