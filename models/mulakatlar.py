from PyQt6.QtWidgets import QMainWindow,  QLabel, QTableWidgetItem
from PyQt6 import uic
from PyQt6.QtCore import Qt
from config.myfunction import *
from config.connectsql import *

class Mulakatlar(QMainWindow):
    def __init__(self, session):
        super().__init__()
        self.session = session
        uic.loadUi("ui_windows/mulakatlar.ui", self)  # Load the Admin Menu UI
        self.myfn = MyAttr()        
        self.setFixedWidth(900)
        self.setFixedHeight(775)

        sorgu = "select kursiyerid, pgondermet, pgelist from projetakip"
        self.mulakatlar = query(sorgu)
        kolon = len(self.mulakatlar[0])
        self.tableWidget.setColumnCount(kolon)
        if self.session.tall == "EN":
            temiz_liste = ['Trainee name',"Project Subm.Date", 'Project Arrival Date']
            self.tumkayitlar_btn.setText("All Records")
            self.projesikomt_btn.setText("Project Arrivals")
            self.projenietkomt_btn.setText("Project Dont Arrivals")
            self.search_inp.setPlaceholderText("enter text to search...")
        elif self.session.tall == "TR":
            temiz_liste = ["Kursiyer","Proje Gönderme T.","Proje Geliş T." ]
            self.exit_btn.setText("Kapat")
        elif self.session.tall == "NL":
            temiz_liste = ["Cursisten","Indieningdatum project","Aankomstdatum project" ]
            self.search_inp.setPlaceholderText("voer tekst in om te zoeken...")
            self.tumkayitlar_btn.setText("Alle Record")
            self.projesikomt_btn.setText("Project Kwamen")
            self.projenietkomt_btn.setText("Project Niet Kwamen")  
            self.exit_btn.setText("Dichtbij")

        self.tableWidget.setHorizontalHeaderLabels(temiz_liste)
        header = self.tableWidget.horizontalHeader()
        header.setSectionsClickable(False)
        self.tableWidget.setRowCount(0) 
        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.setColumnWidth(0, 200)
        self.tableWidget.setColumnWidth(1, 200)
        self.tableWidget.setColumnWidth(2, 200)

        self.exit_btn.clicked.connect(self.exit)
        self.projenietkomt_btn.clicked.connect(self.projenietkomt)
        self.projesikomt_btn.clicked.connect(self.projekomt)
        self.tumkayitlar_btn.clicked.connect(self.tumkayitlar)
        self.search_inp.textChanged.connect(self.filter_search_table)

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


    def tumkayitlar(self):
        self.search_inp.setText("")
        
        self.table_list(self.mulakatlar)


    def projenietkomt(self):
       
        projegelen = []
        for v in self.mulakatlar:
           if v[2] == "":  
                projegelen.append(v)

        self.table_list(projegelen)

    def projekomt(self):
        
        projegelen = []
        for v in self.mulakatlar:
           if v[1] =="":  
                projegelen.append(v)

        self.table_list(projegelen)


    def table_list(self, veri):
        self.tableWidget.setRowCount(0)
        satir = len(veri)
        self.tableWidget.setRowCount(satir)
        for row in range(satir):

            q = "select adsoyad from kursiyerler where kursiyer_id = %s"
            a =(veri[row][0],)
            adsoyad = query(q, a)
            self.tableWidget.setItem(row, 0, QTableWidgetItem(str(adsoyad[0][0])))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(str(veri[row][1])))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(str(veri[row][2])))


    def exit(self):
        self.close()