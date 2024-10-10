from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QPushButton,
    QWidget,
    QMessageBox,
    QCheckBox,
    QGridLayout,
    QLabel,
    QComboBox
)

from sqlite import connect_db

class HAMApp(QMainWindow):
    def __init__(self):

        super().__init__()

        self.setWindowTitle("Home Asset Manager")

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

        # Main widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Table widget
        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        # Columns selection
        self.column_selection = QComboBox()
        self.column_selection.addItems(self.columns)
        self.column_selection.setEditable(False)
        self.layout.addWidget(self.column_selection)

        # Show selected columns
        self.column_checkboxes = {}
        self.checkbox_layout = QGridLayout()
        for index, column in enumerate(self.columns):
            checkbox = QCheckBox(column)
            checkbox.setChecked(True)
            checkbox.stateChanged.connect(self.update_column_visibility)
            self.checkbox_layout.addWidget(checkbox, index // 3, index % 3)
            self.column_checkboxes[column] = checkbox
        self.layout.addLayout(self.checkbox_layout)

        # Buttons
        self.add_button = QPushButton("Add Asset")
        self.add_button.clicked.connect(self.add_asset)
        self.layout.addWidget(self.add_button)

        self.edit_button = QPushButton("Edit Asset")
        self.edit_button.clicked.connect(self.edit_asset)
        self.layout.addWidget(self.edit_button)

        self.load_assets()

    def load_assets(self):
        self.table.setRowCount(0)
        self.table.setColumnCount(len(self.columns))
        self.table.setHorizontalHeaderLabels(self.columns)

        with connect_db() as conn:
            c = conn.cursor()

            c.execute(query)
            for row in c.fetchall():
                row_position = self.table.rowCount()
                self.table.insertRow(row_position)
                for column_index, item in enumerate(row):
                    self.table.setItem(row_position, column_index, QTableWidgetItem(str(item)))
        self.update_column_visibility()

    def update_column_visibility(self):
        for column, checkbox in self.column_checkboxes.items():
            column_index = self.columns.index(column)
            self.table.setColumnHidden(column_index, not checkbox.isChecked())

