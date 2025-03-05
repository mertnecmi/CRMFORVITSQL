from models.login import *  # Import UserLogin and UserSession from models.login
from PyQt6.QtWidgets import QApplication
import sources.my_google_script as goo  # Assuming this is part of your project
from config.myfunction import MyAttr  # Assuming this is part of your project


def main():
    app = QApplication([])

    session = UserSession()  # Create a session object
    login = UserLogin(session)  # Pass session to the constructor of UserLogin
    login.show()

    # Run the application until the login window is closed (we wait for login success)
    app.exec()

