import sys

import sqlite
import gui
from PyQt5.QtWidgets import QApplication


def main():
    sqlite.load_db()
    sqlite.fetch_data()
    app = QApplication(sys.argv)
    window = gui.HAMApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
