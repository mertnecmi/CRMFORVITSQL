from PyQt6.QtWidgets import QMainWindow, QStatusBar, QLabel, QTableWidgetItem
from PyQt6 import uic
from PyQt6.QtCore import Qt
from config.myfunction import *
from config.connectsql import *

class MentorGor(QMainWindow):
    def __init__(self,session):
        super().__init__()
        self.session = session
        uic.loadUi("ui_windows/mentor-gor.ui", self)  # Load the Admin Menu UI
        self.setFixedWidth(1196)
        self.setFixedHeight(721)
        self.myfn = MyAttr()

        #self.mentordata = self.myfn.read_xlsx("data/Mentor.xlsx")
        sorgu = "select gorusmetarihi, kursiyerid, mentoradsoyad, vitprojesinekatilabilirmi, dusunce, yorumlar from mentortablosu"
        self.mentordata = query(sorgu)
        basliklar = ["Tarih","İsim Soyisim", "Mentor","IT Bilgisi","Düşünce","Yorumlar"]
        self.tableWidget.setHorizontalHeaderLabels(basliklar)    
        header = self.tableWidget.horizontalHeader()
        header.setSectionsClickable(False)   
        self.tableWidget.setRowCount(0) 
        self.tableWidget.setColumnWidth(1, 150)
        self.tableWidget.setColumnWidth(2, 150)
        self.tableWidget.setColumnWidth(3, 250)
        self.tableWidget.setColumnWidth(4, 250)
        self.tableWidget.setColumnWidth(5, 250)
        self.cmbboxdoldur()
        print(self.mentordata)

        
        self.comboBox.activated.connect(self.on_item_activated)
        self.tumkayitlar_btn.clicked.connect(self.on_all_kayits)
        self.exit_btn.clicked.connect(self.exit)
        self.search_inp.textChanged.connect(self.filter_search_table)

    def cmbboxdoldur(self):
        self.comboBox.clear()
        cmbdata = set()
        
        for data in self.mentordata:
            cmbdata.add(data[3])
        sorted_list = [""] + sorted(cmbdata)
        self.comboBox.addItems(sorted_list)

    def filter_search_table(self):
        filter_text = self.search_inp.text().lower()  # Girilen metni küçük harfe çevir
        for row in range(self.tableWidget.rowCount()):
            match = False
            for col in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(row, col)
                if item is not None and filter_text in item.text().lower():
                    match = True
                    break  # Eğer bu hücrede eşleşme varsa, satırı göster

            # Eğer eşleşme yoksa satırı gizle
            self.tableWidget.setRowHidden(row, not match)


    def exit(self):
        self.close()

    def on_all_kayits(self):
        self.search_inp.setText("")
        self.cmbboxdoldur()
        self.table_list(self.mentordata)

    def on_item_activated(self):
        cmbchoice = self.comboBox.currentText()
        self.listelenecek = []
        if cmbchoice =="Seçim Yapınız ...":
            pass
        else:
            for d in self.mentordata:
                if d[3] == cmbchoice:
                    self.listelenecek.append(d)
        self.table_list(self.listelenecek)

    def table_list(self, veri):
        self.tableWidget.setRowCount(0)
        satir = len(veri)
        self.tableWidget.setRowCount(satir)
        for row in range(satir):
            q = "select adsoyad from kursiyerler where kursiyer_id = %s"
            a =(veri[row][1],)
            adsoyad = query(q, a)
            self.tableWidget.setItem(row, 0, QTableWidgetItem(str(veri[row][0])))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(str(adsoyad[0][0])))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(str(veri[row][2])))
            self.tableWidget.setItem(row, 3, QTableWidgetItem(str(veri[row][3])))
            self.tableWidget.setItem(row, 4, QTableWidgetItem(str(veri[row][4])))
            self.tableWidget.setItem(row, 5, QTableWidgetItem(str(veri[row][5])))


