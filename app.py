import tkinter as tk

import sqlite
import gui


def main():
    sqlite.load_db()
    sqlite.fetch_data()
    root = tk.Tk()
    app = gui.HAMApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
