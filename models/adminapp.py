from PyQt6.QtWidgets import QMainWindow,QTableWidgetItem

from PyQt6 import uic
from PyQt6.QtGui import QColor
from config.myfunction import *
from sources.my_google_calendar import *
from sources.my_google_mail import *
from sources.my_google_script import *

class AdminApp(QMainWindow):
    def __init__(self,session):
        super().__init__()
        self.session = session
        uic.loadUi("ui_windows/admin-app.ui", self)  # Load the Admin Menu UI
        self.myfn = MyAttr()
        self.setFixedWidth(1025)
        self.setFixedHeight(592)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.setColumnWidth(0, 250)
        self.tableWidget.setColumnWidth(1, 100)
        self.tableWidget.setColumnWidth(2, 150)

        header=["ETKİNLİK ADI","ETKİNLİK ZAMANI", "ORGANİZATOR MAİL","KATILIMCI MAİL"]
        self.tableWidget.setHorizontalHeaderLabels(header)

        self.exit_btn.clicked.connect(self.exit)
        self.email_btn.clicked.connect(self.email)
        self.event_btn.clicked.connect(self.events)
        #self.xlsupdate_btn.clicked.connect(self.xlsupdate)
        ##self.tableWidget.itemClicked.connect(self.highlight_row)

    def xlsupdate(self):
        dosyakontrol = main()
        self.label_3.setText(dosyakontrol)

    def events(self):
        event = get_google_calendar_events()
        veriler = []
        for e in event:
            veri = []  # her etkinlik için veriyi sıfırla
            veri.append(e["summary"])  # Etkinlik başlığını ekle
            veri.append(e["start"])    # Etkinlik başlangıç zamanını ekle
            
            attendees_emails = []

            for attendee in e["attendees"]:
                if "email" in attendee and attendee["email"]:
                    attendees_emails.append(attendee["email"])  # Katılımcının e-postasını ekle

            # attendees_emails listesini veri listesine tek bir eleman olarak ekle
            veri.append(attendees_emails)
            veriler.append(veri)  # Etkinlik verisini ana listeye ekle


        row = len(veriler)

        self.tableWidget.setRowCount(row)   
        for row in range(len(veriler)):  # data verilerinizi temsil eder
            # İlk hücreyi set ediyoruz
            self.tableWidget.setItem(row, 0, QTableWidgetItem(str(veriler[row][0])))

            # İkinci hücreyi set ediyoruz
            self.tableWidget.setItem(row, 1, QTableWidgetItem(str(veriler[row][1])))

            # Eğer veriler[row][2] (katılımcı e-postaları) listesi boş değilse
            if veriler[row][2]:
                # İlk katılımcının e-posta adresini ekliyoruz
                self.tableWidget.setItem(row, 2, QTableWidgetItem(str(veriler[row][2][0])))
    
            # Eğer geri kalan katılımcılar varsa
            if len(veriler[row][2]) > 1:
                    # Geri kalan e-posta adreslerini birleştirerek ekliyoruz
                self.tableWidget.setItem(row, 3, QTableWidgetItem(str(veriler[row][2][1:])))
            else:
                # Eğer geri kalan katılımcı yoksa boş bırakıyoruz
                self.tableWidget.setItem(row, 3, QTableWidgetItem(""))
        else:
            
            self.tableWidget.setItem(row, 2, QTableWidgetItem(""))
            self.tableWidget.setItem(row, 3, QTableWidgetItem(""))


    def email(self):
        self.label_3.setText("")
        data = self.get_selected_row_data()
        if data:
            print(data)
            if len(data[3]) > 0:
                
                subject = f"Yeni Etkinlik: {data[0]}"
                body = f"Merhaba,\n\nYeni etkinlik hakkında bilgilendirme:\n\nEtkinlik: {data[0]}\nBaşlangıç: {data[1]}\nAçıklama: ..."

                # E-posta gönder
                mailgonder = send_email(subject, body, data[3].strip("[]").replace("'", ""))
                self.label_3.setText(mailgonder)
                print(mailgonder)
            else:
                self.label_3.setText("mail yok")
        else:
            self.label_3.setText("Seçilen Etkinlik mail adresi yok")

    def exit(self):
        self.close()

    def get_selected_row_data(self):
        selected_row = self.tableWidget.currentRow()  # Tıklanan satırın index'ini al
        row_data = []  # Tıklanan satırdaki verileri tutacağımız liste
        self.label_3.setText(str(selected_row))
        # Eğer bir satır seçildiyse
        if selected_row > -1 :
            for column in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(selected_row, column)  # Hücre verisini al
                row_data.append(item.text() if item else '')  # Eğer hücrede veri varsa, ekle
            return row_data
        else:
            return False
        

    def highlight_row(self, item):
        # Tıklanan hücrenin satır numarasını al
        row = item.row()

        # Satırdaki tüm hücrelerin rengini değiştir
        for column in range(self.tableWidget.columnCount()):
            cell = self.tableWidget.item(row, column)
            if cell:
                # Hücreyi sarı renkte yapıyoruz
                cell.setBackground(QColor(0, 180, 200))

        # Diğer satırlardaki hücrelerin rengini eski haline getirme (isteğe bağlı)
        for r in range(self.tableWidget.rowCount()):
            if r != row:
                for c in range(self.tableWidget.columnCount()):
                    cell = self.tableWidget.item(r, c)
                    if cell:
                        cell.setBackground(QColor(255, 255, 255))  # Beyaz (normal renk)