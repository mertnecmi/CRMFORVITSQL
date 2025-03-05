from PyQt6.QtWidgets import QMainWindow, QStatusBar, QLabel, QTableWidgetItem
from PyQt6 import uic
from PyQt6.QtCore import Qt
from config.myfunction import *
from config.connectsql import * 

class Basvurular(QMainWindow):
    def __init__(self,session):
        super().__init__()
        self.session = session
        uic.loadUi("ui_windows/basvurular.ui", self)  # Load the Admin Menu UI
        self.myfn = MyAttr()
        self.setFixedWidth(1500)
        self.setFixedHeight(768)


        # Tabloyu sıralanabilir yapma
        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.setColumnWidth(0, 120)
        self.tableWidget.setColumnWidth(1, 150)
        self.tableWidget.setColumnWidth(2, 170)
        self.tableWidget.setColumnWidth(4, 70)
        self.tableWidget.setColumnWidth(6, 250)
        self.tableWidget.setColumnWidth(7, 250)


        sorgu = "select * from basvurular"
        self.basvurular = query(sorgu)

        kolon = len(self.basvurular[0])
        self.tableWidget.setColumnCount(kolon)
        q = """SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'basvurular'
            ORDER BY ordinal_position"""
        header = query(q)
        header = list(header)
        temiz_liste = [kolon[0] for kolon in header]
        temiz_liste[1] = "Kursiyer"
        self.tableWidget.setHorizontalHeaderLabels(temiz_liste)
        header = self.tableWidget.horizontalHeader()
        header.setSectionsClickable(False)  # Başlıkların tıklanabilirliğini devre dışı bırakıyoruz
        self.tableWidget.setRowCount(0) 

        self.definementmeet_btn.clicked.connect(self.tanimlananMentorGor)
        self.tgeenmgorusmeleri_btn.clicked.connect(self.tgeenmgorusmeleri)
        self.tumkayitlar_btn.clicked.connect(self.tum_kayitlar)
        self.different_btn.clicked.connect(self.filter_defferent_rows)
        self.same_btn.clicked.connect(self.filter_same_rows) #mükerrer Kayıt
        self.samefilter_btn.clicked.connect(self.sameFilter) #başvuru filtreli
        self.oncekivit_btn.clicked.connect(self.oncekivit)
        
        
        
        # arama inputuna birşy girildiğinde
        self.search_inp.textChanged.connect(self.filter_search_table)
        
        
        

        self.exit_btn.clicked.connect(self.exit)


    def filter_defferent_rows(self):
        self.tableWidget.clearContents()
        self.tablo_listele( "farkli")
        self.label_5.setText("FARKLI KAYITLAR")


    def oncekivit(self):
        self.tableWidget.clearContents()
        self.tablo_listele( "onceki")
        self.label_5.setText("ONCEKİ VIT KAYITLARI")

    def tum_kayitlar(self):
        self.tableWidget.clearContents()
        self.search_inp.setText("")
        self.tablo_listele( "tumu")
        self.label_5.setText("TÜM KAYITLAR")

    def tgeenmgorusmeleri(self):
        self.tableWidget.clearContents()
        self.tablo_listele( "atanmadi")
        self.label_5.setText("TANIMLANMAYAN MENTOR GORUSMELERI")

    def tanimlananMentorGor(self):
        self.tableWidget.clearContents()
        self.tablo_listele( "mentortanimlandi")
        self.label_5.setText("TANIMLANAN MENTOR GORUSMELERI")

    #arama modulu
    def filter_search_table(self):

        filter_text = self.search_inp.text().lower()  # Girilen metni küçük harfe çevir
        self.label_5.setText("ÖZEL ARAMA")
        for row in range(self.tableWidget.rowCount()):
            match = False
            for col in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(row, col)
                if item is not None and filter_text in item.text().lower():
                    match = True
                    break  # Eğer bu hücrede eşleşme varsa, satırı göster

            # Eğer eşleşme yoksa satırı gizle
            self.tableWidget.setRowHidden(row, not match)



    def sameFilter(self):  #başvuru filtreli
        self.tableWidget.clearContents()
        self.label_5.setText("FİLTRELENMİŞ BAŞVURULAR")
        
        seen = set()
        unique_data = []

        for record in self.basvurular:
            if record[1] not in seen:
                unique_data.append(record)
                seen.add(record[1])

        self.xtable_list(unique_data)

    def filter_same_rows(self):
        self.label_5.setText("MÜKERRER KAYITLAR")
        seen = set()  # Bu set, daha önce gördüğümüz değerleri tutacak
        unique_data = []  # Bu liste, mükerrer kayıtları tutacak

        for record in self.basvurular:  # self.basvurular her bir başvuru satırını temsil ediyor
            if record[1] in seen:  # Eğer başvurunun 1. indeksindeki değer daha önce göründüyse
                unique_data.append(record)  # Bu satır tekrarlayan bir kayıt olduğundan unique_data'ya eklenir
            seen.add(record[1])  # Bu satırdaki 1. indeks değerini set'e ekleriz (ilk kez görüyorsak)

        self.xtable_list(unique_data) 


    def xtable_list(self, veri):
        # Satır sayısını güncelle
        veri.sort(key=lambda x: x[1])
        self.tableWidget.setRowCount(0)  # Tabloyu sıfırla
        
        # Toplam kayıt sayısını kaydet
        row_count = len(veri)
        self.tableWidget.setRowCount(row_count)  # Yeni satır sayısını ayarla
        
        # Her bir satırı ve sütunu doldur
        for row_idx, row in enumerate(veri):  # veri içindeki her bir satırı temsil eden döngü
            for col_idx, value in enumerate(row):  # Her bir satırdaki her sütunu temsil eden döngü
                if col_idx == 1:
                    sorgu = "select adsoyad from kursiyerler where kursiyer_id = %s"
                    a =(value,)
                    adsoyad = query(sorgu, a)
                   
                    self.tableWidget.setItem(row_idx, col_idx, QTableWidgetItem(str(adsoyad[0][0])))
                elif col_idx == 16:  # Eğer ilk sütunsa, tarih formatını değiştir
                    tarih = self.myfn.tarih_format_degistir(value)
                    self.tableWidget.setItem(row_idx, col_idx, QTableWidgetItem(str(tarih)))
                else:
                    self.tableWidget.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))


    def tablo_listele(self, neler="tumu"):
        self.tableWidget.setRowCount(0)
        satir = 0
        yenibasvurulist = []
        if neler == "mentortanimlandi":
            for basvuru in self.basvurular:
                if basvuru[17] == "OK":
                    yenibasvurulist.append(basvuru)
        elif neler =="onceki":
            for basvuru in self.basvurular:
                if basvuru[15] != "VIT3":
                    yenibasvurulist.append(basvuru)
        elif neler =="farkli":
            for basvuru in self.basvurular:
                if basvuru[15] == "VIT3":
                    yenibasvurulist.append(basvuru)
        elif neler =="vit3":
            for basvuru in self.basvurular:
                if basvuru[15] == "VIT3":
                    yenibasvurulist.append(basvuru)
        elif neler =="tumu":
            for basvuru in self.basvurular:
                yenibasvurulist.append(basvuru)
        elif neler =="atanmadi":
            for basvuru in self.basvurular:
                if basvuru[17] == "ATANMADI":
                    yenibasvurulist.append(basvuru)

        row = len(yenibasvurulist)
        self.tableWidget.setRowCount(row)
        yenibasvurulist.sort(key=lambda x: x[1])
        # Verileri tabloya eklemek
        for row in range(len(yenibasvurulist)):  # data verilerinizi temsil eder
            satir +=1
            for col in range(len(yenibasvurulist[row])):
                if col == 1:
                    sorgu = "select adsoyad from kursiyerler where kursiyer_id = %s"
                    a =(yenibasvurulist[row][col],)
                  
                    adsoyad = query(sorgu, a)
                    
                    duz_liste = [item[0] for item in adsoyad]
                   
                    self.tableWidget.setItem(row, col, QTableWidgetItem(str(duz_liste[0])))
                elif col == 16:
                    tarih = self.myfn.tarih_format_degistir(yenibasvurulist[row][col])
                    self.tableWidget.setItem(row, col, QTableWidgetItem(str(tarih)))
                else:
                    self.tableWidget.setItem(row, col, QTableWidgetItem(str(yenibasvurulist[row][col])))

                
     
    def exit(self):
        self.close()
