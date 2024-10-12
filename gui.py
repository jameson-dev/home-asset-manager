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
            query = """
            SELECT
                a.asset_number,
                l.name AS locations_name,
                t.name AS type_name,
                m.name AS model_name,
                a.serial_number,
                a.ip_address
            FROM
                assets a
            JOIN
                types t ON a.type_id = t.id
            JOIN
                models m ON a.model_id = m.id
            JOIN
                locations l ON a.location_id = l.id;
            """

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

    def add_asset(self):
        # Open dialog window to add new asset
        self.asset_dialog("Add Asset")

    def edit_asset(self):
        selected_items = self.table.selectedItems()
        if selected_items:
            asset_number = selected_items[0].text()
            self.asset_dialog("Edit Dialog", asset_number)
        else:
            QMessageBox.warning(self, "Select Asset", "Please select an asset to edit.")

    def asset_dialog(self, title, asset_number=None):
        dialog = QWidget
        dialog.setWindowTitle(title)
        dialog_layout = QGridLayout(dialog)

        dialog_layout.addWidget(QLabel("Asset Number"), 0, 0)
        asset_number_input = QTableWidgetItem()
        dialog_layout.addWidget(asset_number_input, 0, 1)

        dialog_layout.addWidget(QLabel("Type ID"), 1, 0)
        type_id_input = QTableWidgetItem()
        dialog_layout.addWidget(type_id_input, 1, 1)

        dialog_layout.addWidget(QLabel("Model ID"), 2, 0)
        model_id_input = QTableWidgetItem()
        dialog_layout.addWidget(model_id_input, 2, 1)

        dialog_layout.addWidget(QLabel("Location ID"), 3, 0)
        location_id_input = QTableWidgetItem()
        dialog_layout.addWidget(location_id_input, 3, 1)

        dialog_layout.addWidget(QLabel("Serial Number"), 4, 0)
        serial_number_input = QTableWidgetItem()
        dialog_layout.addWidget(serial_number_input, 4, 1)

        dialog_layout.addWidget(QLabel("IP Address"), 5, 0)
        ip_address_input = QTableWidgetItem()
        dialog_layout.addWidget(ip_address_input, 5, 1)

        if asset_number:
            # Load existing asset data
                with connect_db() as conn:
                    c = conn.cursor()
                    c.execute("SELECT type_id, model_id, location_id, serial_number, ip_address FROM assets WHERE asset_number = ?", (asset_number,))
                    data = c.fetchone()
                    if data:
                        type_id_input.setText(str(data[0]))
                        model_id_input.setText(str(data[1]))
                        location_id_input.setText(str(data[2]))
                        serial_number_input.setText(data[3])
                        ip_address_input.setText(data[4])

        save_button = QPushButton("Save")
        save_button.clicked.connect(lambda: self.save_asset(asset_number, asset_number_input.text(), type_id_input.text(), model_id_input.text(), location_id_input.text(), serial_number_input.text(), ip_address_input.text()))
        dialog_layout.addWidget(save_button, 6, 0, 1, 2)

        dialog.setLayout(dialog_layout)
        dialog.show()

    def save_asset(self, old_asset_number, asset_number, type_id, model_id, location_id, serial_number, ip_address):
        with connect_db() as conn:
            c = conn.cursor()
            if old_asset_number:
                # Update existing asset
                c.execute('''
                UPDATE assets 
                SET asset_number = ?, type_id = ?, model_id = ?, location_id = ?, serial_number = ?, ip_address = ? 
                WHERE asset_number = ?
                ''', (asset_number, type_id, model_id, location_id, serial_number, ip_address, old_asset_number))
            else:
                # Insert new asset
                c.execute('''
                INSERT INTO assets (asset_number, type_id, model_id, location_id, serial_number, ip_address) 
                VALUES (?, ?, ?, ?, ?, ?)
                ''', (asset_number, type_id, model_id, location_id, serial_number, ip_address))

            conn.commit()
            self.load_assets()
            QMessageBox.information(self, "Success", "Asset saved successfully.")