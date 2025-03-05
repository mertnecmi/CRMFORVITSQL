from PyQt6.QtWidgets import QMainWindow, QStatusBar, QLabel
from PyQt6 import uic
from PyQt6.QtCore import Qt
from config.myfunction import *
from models.basvurular import Basvurular
from models.mentor import MentorGor
from models.mulakatlar import Mulakatlar
from models.adminapp import AdminApp


class AdminMenu(QMainWindow):
    def __init__(self,session):
        super().__init__()
        self.session = session
        uic.loadUi("ui_windows/admin-menu.ui", self)  # Load the Admin Menu UI
        self.myfn = MyAttr()
        self.setFixedWidth(612)
        self.setFixedHeight(486)
        self.exit_btn.clicked.connect(self.exit)
        self.basvurular_btn.clicked.connect(self.basvurular)
        self.mentorgo_btn.clicked.connect(self.mentorGorusmeleri)
        self.mulakatlar_btn.clicked.connect(self.mulakatlar)
        self.adminapp_btn.clicked.connect(self.adminApp)

    def adminApp(self):
        self.adminappWin = AdminApp(self.session)
        self.adminappWin.show()


    def mulakatlar(self):
        self.mulakatlarWin = Mulakatlar(self.session)
        self.mulakatlarWin.show()

    def mentorGorusmeleri(self):
        self.basvurularWin = MentorGor(self.session)
        self.basvurularWin.show()

    def basvurular(self):
        self.basvurularWin = Basvurular(self.session)
        self.basvurularWin.show()

    def exit(self):
        # Override the closeEvent to control the window closing behavior
        print("Admin menu is closing...")
        self.close()
