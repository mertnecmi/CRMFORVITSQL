from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow
from models.user_menu import UserMenu  # Import UserMenu
from models.admin_menu import AdminMenu  # Import AdminMenu
from config.myfunction import MyAttr
from config.connectsql import *
# Kullanıcı oturumu (session) yönetimi

class UserSession:
    def __init__(self):
        self.userauth = None  # The user authorization (None, 'admin', 'user', etc.)
        self.username = None  # The username of the logged-in user
        self.tall = "EN"

# Login işlemi yapacak sınıf
class UserLogin(QMainWindow):
    def __init__(self, session):  # Accept session as a parameter
        super().__init__()
        uic.loadUi("ui_windows/login.ui", self)  # Load the login UI
        self.session = session  # Store session object
        self.setFixedWidth(661)
        self.setFixedHeight(453)
        self.tr_TR.clicked.connect(self.taal_call_tr)
        self.nl_NL.clicked.connect(self.taal_call_nl)
        self.en_EN.clicked.connect(self.taal_call_en)
        self.username_inp.setFocus()  # Set focus to the username input field
        self.password_inp.returnPressed.connect(self.login_click)
        # Connect button actions
        self.exit_btn.clicked.connect(self.exit_click)
        self.login_btn.clicked.connect(self.login_click)

    def taal_call_en(self):
        self.session.tall = "EN"
        self.Crmlogin_lbl.setText("CRM Login")
        self.username_lbl.setText("Username")
        self.password_lbl.setText("Password")
        self.exit_btn.setText("Exit")
        self.login_btn.setText("Login")
    def taal_call_nl(self):
        self.session.tall = "NL"
        self.Crmlogin_lbl.setText("CRM INLOG")
        self.username_lbl.setText("Gebruiker")
        self.password_lbl.setText("Wachtwoord")
        self.exit_btn.setText("Uitgang")
        self.login_btn.setText("Ingang")
    def taal_call_tr(self):
        self.session.tall = "TR"
        self.Crmlogin_lbl.setText("CRM GİRİŞ")
        self.username_lbl.setText("Kullanıcı Adı")
        self.password_lbl.setText("Şifre")
        self.exit_btn.setText("Çıkış")
        self.login_btn.setText("Giriş")
    def exit_click(self):
        self.close()  # Close the application when the exit button is clicked
    def mesaj_yaz(self, mesaj):
        if mesaj == "bosolamaz":
            if self.session.tall == "TR":
                self.mesaj_lbl.setText("Kullanıcı Adı ve Şifre Boş Olamaz...!")
            if self.session.tall == "NL":
                self.mesaj_lbl.setText("Gebruikersnaam en wachtwoord mogen niet leeg zijn")
            if self.session.tall == "EN":
                self.mesaj_lbl.setText("Username and Password Cannot Be Blank")
        if mesaj == "hata":
            if self.session.tall == "TR":
                self.mesaj_lbl.setText("Kullanıcı Adı ve Şifre Hatası...!")
            if self.session.tall == "NL":
                self.mesaj_lbl.setText("Gebruikersnaam en wachtwoord Fout..!")
            if self.session.tall == "EN":
                self.mesaj_lbl.setText("Username and Password Wrong")
    def login_click(self):
        username = self.username_inp.text()
        password = self.password_inp.text()
        if username =="" or password == "":
            self.mesaj_yaz("bosolamaz")
        else:
            sorgu = "select * from kullanicilar"  
            users = query(sorgu)
            #conn.close()
  
            for user in users:
            # Simple login validation (you can extend this with real authentication)
                if username.lower() == user[1] and password == user[2]:
                    self.session.username = username  # Set the username in the session
                    self.session.userauth = user[3] # Set the user role as "admin" (this can be dynamic based on the user)
                    if self.session.userauth == "admin":
                        self.adminmenu = AdminMenu(self.session)
                        self.adminmenu.show()
                        self.close()
                    elif self.session.userauth == "user":
                        self.adminmenu = UserMenu(self.session)
                        self.adminmenu.show()
                        self.close()
                    else:
                        self.mesaj_lbl.setText("Wrong Auth...")
                        break
                else:
                    self.mesaj_yaz("hata")  # Display error message if login fails
