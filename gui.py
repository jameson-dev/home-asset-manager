import tkinter as tk
from tkinter import ttk


class HAMApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Home Asset Manager")

        # Set columns and make all visible
        self.columns = ["Asset #",
                        "Location",
                        "Type",
                        "Model",
                        "Serial Number",
                        "IP Address",
                        "Purchase Date",
                        "Warranty Expiration",
                        "Notes"]
        self.visible_cols = self.columns.copy()

        # Create Treeview
        self.tree = ttk.Treeview(root, columns=self.columns, show='headings')
        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, stretch=tk.YES, width=100)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Create column selection
        self.column_selection = tk.StringVar(value="Select columns")
        self.column_dropdown = ttk.Combobox(root, textvariable=self.column_selection, values=self.columns)
        self.column_dropdown.pack(side=tk.LEFT, padx=10)
        self.column_dropdown.bind("<<ComboboxSelected>>", self.toggle_column)

    def toggle_column(self, event):
        selected_column = self.column_selection.get()
        if selected_column in self.visible_cols:
            self.visible_cols.remove(selected_column)
        else:
            self.visible_cols.append(selected_column)
        self.update_column_visibility()

    def update_column_visibility(self):
        for col in self.columns:
            if col in self.visible_cols:
                self.tree.heading(col, text=col)
                self.tree.column(col, stretch=tk.YES, width=100)
            else:
                self.tree.heading(col, text="")
                self.tree.column(col, width=0)