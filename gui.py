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

        # # Create column selection
        # self.column_selection = tk.StringVar(value="Select columns")
        # self.column_dropdown = ttk.Combobox(root, textvariable=self.column_selection, values=self.columns)
        # self.column_dropdown.pack(side=tk.LEFT, padx=10)
        # self.column_dropdown.bind("<<ComboboxSelected>>", self.toggle_column)

        # Create columns selection listbox
        self.column_selection_frame = tk.Frame(root)
        self.column_selection_frame.pack(side=tk.LEFT, padx=10)

        self.column_listbox = tk.Listbox(self.column_selection_frame, selectmode=tk.MULTIPLE)
        for col in self.columns:
            self.column_listbox.insert(tk.END, col)

        # Pre-select already visible columns
        for index, col in enumerate(self.columns):
            if col in self.visible_cols:
                self.column_listbox.select_set(index)

        self.column_listbox.pack()

        self.column_listbox.bind("<<ListboxSelect>>", self.update_visible_cols)

    def update_visible_cols(self, event):
        selected_indices = self.column_listbox.curselection()
        self.visible_cols = [self.column_listbox.get(i) for i in selected_indices]
        self.update_column_visibility()

    def update_column_visibility(self):
        for col in self.columns:
            if col in self.visible_cols:
                self.tree.heading(col, text=col)
                self.tree.column(col, stretch=tk.YES, width=100)
            else:
                self.tree.heading(col, text="")
                self.tree.column(col, width=0)