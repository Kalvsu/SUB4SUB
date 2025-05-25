
import json
import logging
import os
import random
import threading
import time
import traceback
from datetime import datetime
import requests
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor, QFont, QIcon, QPalette, QPixmap
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QScrollArea, QLabel, \
    QPushButton, QHBoxLayout, QSizePolicy, QGroupBox, QTableWidget, QTableWidgetItem, QHeaderView, QDialog, \
    QLineEdit, QMessageBox, QFrame, QTextEdit, QSplitter, QFileDialog, QCheckBox
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import activetasktab
import dashboard
import tabdesign
import createtask

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window title and size
        self.setWindowTitle("SUB4SUB")
        self.setGeometry(100, 100, 1200, 600)

        # Variables for handling window movement
        self.is_moving = False
        self.window_position = None
        self.mouse_position = None

        # Create a QFrame to hold the main content
        frame = QFrame(self)
        frame.setFrameStyle(QFrame.Panel | QFrame.Raised)
        frame.setLineWidth(1)
        frame.setAutoFillBackground(True)
        frame.setBackgroundRole(QPalette.Window)

        # Create a QVBoxLayout for the frame
        frame_layout = QVBoxLayout(frame)
        frame_layout.setContentsMargins(0, 0, 0, 0)

        # Create a CoolTabWidget
        self.tab_widget = tabdesign.CoolTabWidget()

        # Create three tabs
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()

        # Add tabs to the tab widget
        self.tab_widget.addTab(self.tab1, "DASHBOARD")
        self.tab_widget.addTab(self.tab2, "ACCOUNT MANAGER")
        self.tab_widget.addTab(self.tab3, "CREATE TASK")
        self.tab_widget.addTab(self.tab4, "ACTIVE TASK")


        self.tab_widget.tabBarClicked.connect(self.tab_clicked)

        self.setCentralWidget(self.tab_widget)

        # Set layout for each tab
        self.tab1.layout = QVBoxLayout(self.tab1)
        self.tab2.layout = QVBoxLayout(self.tab2)
        self.tab3.layout = QVBoxLayout(self.tab3)
        self.tab4.layout = QVBoxLayout(self.tab4)

        # Add a scroll area to each tab
        self.tab1.scroll_area = QScrollArea(self.tab1)
        self.tab2.scroll_area = QScrollArea(self.tab2)
        self.tab3.scroll_area = QScrollArea(self.tab3)
        self.tab4.scroll_area = QScrollArea(self.tab4)

        # Set the layout for each scroll area
        self.tab1.layout.addWidget(self.tab1.scroll_area)
        self.tab2.layout.addWidget(self.tab2.scroll_area)
        self.tab3.layout.addWidget(self.tab3.scroll_area)
        self.tab4.layout.addWidget(self.tab4.scroll_area)

        # Set the scroll area widget resizable and auto-scrolling
        self.tab1.scroll_area.setWidgetResizable(True)
        self.tab2.scroll_area.setWidgetResizable(True)
        self.tab3.scroll_area.setWidgetResizable(True)
        self.tab4.scroll_area.setWidgetResizable(True)

        setupscrollarea = self.tab3.scroll_area
        # Set up labels inside scroll areas for demonstration
        self.setup_account_manager(self.tab2.scroll_area)
        createtask.setup_account_list_run(self, setupscrollarea)
        activetasktab.setup_active_task(self)
        dashboard.add_dashboard_boxes(self)


        # Set the layout for each tab widget
        self.tab1.setLayout(self.tab1.layout)
        self.tab2.setLayout(self.tab2.layout)
        self.tab3.setLayout(self.tab3.layout)
        self.tab4.setLayout(self.tab4.layout)

        # Set the central widget as the tab widget
        frame_layout.addWidget(self.tab_widget)

        # Add the frame to the main window
        self.setCentralWidget(frame)

        # Set font and font size for the tab labels
        font = QFont("Arial", 14)
        self.tab_widget.setFont(font)

        # Set the application style
        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #f2f2f2;
            }
            """
        )

        # Customize window buttons
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.create_window_buttons()



        # Add resizable corner widget
        self.resizable_corner = tabdesign.ResizableCorner(self)
        self.resizable_corner.move(self.width() - 20, self.height() - 20)
        self.resizable_corner.show()



    def tab_clicked(self, index):
        if index == 2:  # Check if "create task" tab is clicked
            self.setGeometry(self.x(), self.y(), 1200, 600)

        elif index == 3:
            self.setGeometry(self.x(), self.y(), 1200, 600)

        elif index == 0:
            self.setGeometry(self.x(), self.y(), 850, 600)

        elif index == 1:
            self.setGeometry(self.x(), self.y(), 850, 600)


    ##############################################
    #RESIZE EVENTS                               #
    ##############################################
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.reposition_resizable_corner()
    def reposition_resizable_corner(self):
        self.resizable_corner.move(self.width() - 20, self.height() - 20)
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.reposition_resizable_corner()
    def reposition_resizable_corner(self):
        self.resizable_corner.move(self.width() - 20, self.height() - 20)
    ##############################################

    ##############################################
    # SETUP ACCOUNT MANAGER                      #
    ##############################################
    def setup_account_manager(self, scroll_area):
        # Create a group box to hold the table and buttons
        group_box = QGroupBox()
        group_box.setStyleSheet(
            """
            QGroupBox {
                border: 1px solid #cfd8dc;
                border-radius: 5px;
                background-color: #fafafa;
                margin-bottom: 10px;  /* Add margin at the bottom */
            }
            """
        )

        # Create a layout for the group box
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        group_box.setLayout(layout)

        # Create a note label for the verified accounts
        note_label = QLabel("VERIFIED = THE GMAIL ACCOUNT IS ACCESSIBLE, MEANING THERE IS NO BYPASS PROTECTION.")
        note_label.setStyleSheet(
            """
            QLabel {
                font-family: Arial;
                font-size: 12px;
                font-weight: bold;
                color: #555555;
                margin-bottom: 10px;
                border: none;  /* Remove the border */
                background-color: transparent;  /* Set transparent background */
            }
            """
        )

        # Add the note label to the layout
        layout.addWidget(note_label)


        # Create a table widget for the account manager
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(4)  # Add an extra column for the checkboxes
        self.table_widget.setHorizontalHeaderLabels(["Gmail", "Password", "Verified", "YouTube Status"])

        # Set the table to be uneditable
        self.table_widget.setEditTriggers(QTableWidget.NoEditTriggers)

        # Set the table selection behavior to select entire rows
        self.table_widget.setSelectionBehavior(QTableWidget.SelectRows)

        # Set the stretch mode for the last column to make it stretch to the end
        header = self.table_widget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        # Add widgets to the layout
        layout.addWidget(self.table_widget)

        # Create a small account checker logs box
        logs_box = QGroupBox()
        logs_box.setStyleSheet(
            """
            QGroupBox {
                border: 1px solid #000000;
                border-radius: 5px;
                background-color: #ffffff;
                padding: 10px;  /* Add padding for better visibility */
            }
            QGroupBox QLabel {
                font-family: Arial;
                font-size: 14px;  /* Increase the font size for better visibility */
                font-weight: bold;
                color: #000000;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 4px;
                border-top: 2px solid #000000;
                background-color: #f2f2f2;  /* Add a background color for a cooler effect */
                border-radius: 5px;  /* Add border radius for a rounded look */
                margin-top: -10px;  /* Adjust the margin-top for a raised appearance */
            }
            """
        )
        logs_box.setTitle("")
        logs_layout = QVBoxLayout(logs_box)

        # Create a QLabel for the title
        title_label = QLabel("Account Checker (logs) :")

        # Add the title label to the layout
        logs_layout.addWidget(title_label)

        # Create a text edit for the logs
        self.logs_text = QTextEdit()  # Make logs_text an instance variable
        self.logs_text.setReadOnly(True)
        self.logs_text.setStyleSheet(
            """
            QTextEdit {
                font-family: Arial;
                font-size: 12px;
                color: #333333;
                background-color: #ffffff;
                border: none;
            }
            """
        )

        # Apply bold style to the logs text
        logs_font = self.logs_text.font()
        logs_font.setBold(True)
        self.logs_text.setFont(logs_font)

        # Create a scroll area for the logs
        logs_scroll_area = QScrollArea()
        logs_scroll_area.setWidgetResizable(True)

        # Set the initial size of the scroll area
        logs_scroll_area.setMinimumHeight(200)  # Adjust the height as needed

        # Set the logs text as the widget inside the scroll area
        logs_scroll_area.setWidget(self.logs_text)

        # Set the size policy for the logs box
        logs_box.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)

        # Add the logs scroll area to the logs box
        logs_layout.addWidget(logs_scroll_area)

        # Add the logs box to the layout
        layout.addWidget(logs_box)

        # Create a checkbox for "DELETE ACCOUNT IF INVALID"
        self.delete_checkbox = QCheckBox("DELETE ACCOUNT IF INVALID")
        self.delete_checkbox.setStyleSheet(
            """
            QCheckBox {
                font-family: Arial;
                font-size: 12px;
                color: #555555;
                background-color: transparent;
            }
            """
        )

        # Create a checkbox for "DELETE ACCOUNT IF INVALID"
        self.notheadless = QCheckBox("NOT HEADLESS (YOU CAN SEE CHROME ACTIVITY)")
        self.notheadless.setStyleSheet(
            """
            QCheckBox {
                font-family: Arial;
                font-size: 12px;
                color: #555555;
                background-color: transparent;
            }
            """
        )

        # Add the checkbox to the layout
        layout.addWidget(self.delete_checkbox)
        layout.addWidget(self.notheadless)

        # Create "SAVE ALL VERIFIED ACCOUNTS" button
        save_verified_button = QPushButton("SAVE ALL VERIFIED ACCOUNTS")
        save_verified_button.setStyleSheet(
            """
            QPushButton {
                background-color: #ffeb3b;
                color: #000000;
                border: none;
                border-radius: 3px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #fdd835;
            }
            """
        )

        # Create a QLabel for the note
        note_label = QLabel("Saved accounts will appear on the Create Task tab.")

        # Add the "SAVE ALL VERIFIED ACCOUNTS" button and note to the layout
        layout.addWidget(save_verified_button)
        layout.addWidget(note_label)


        # Create "ADD ACCOUNT" button
        add_account_button = QPushButton("ADD ACCOUNT")
        add_account_button.setStyleSheet(
            """
            QPushButton {
                background-color: #4caf50;
                color: #ffffff;
                border: none;
                border-radius: 3px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            """
        )

        # Create "ADD ACCOUNT" button
        delete_account = QPushButton("DELETE ACCOUNT")
        delete_account.setStyleSheet(
            """
            QPushButton {
                background-color: #4caf50;
                color: #ffffff;
                border: none;
                border-radius: 3px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            """
        )

        # Create checkbox for checking YT status
        self.check_yt_status_checkbox = QCheckBox("CHECK YT STATUS TOO")
        self.create_channel_checkbox = QCheckBox("AUTO CREATE CHANNEL IF NONE (RANDOM NAME)")

        # Create "CHECK ACCOUNTS" button
        check_accounts_button = QPushButton("CHECK ACCOUNT")
        check_accounts_button.setStyleSheet(
            """
            QPushButton {
                background-color: #2196f3;
                color: #ffffff;
                border: none;
                border-radius: 3px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1e88e5;
            }
            """
        )

        # Create "CHECK ALL NON VERIFIED" button
        check_all_button = QPushButton("CHECK ALL NON VERIFIED")
        check_all_button.setStyleSheet(
            """
            QPushButton {
                background-color: #ff9800;
                color: #ffffff;
                border: none;
                border-radius: 3px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #f57c00;
            }
            """
        )

        # Create "IMPORT ACCOUNTS" button
        import_accounts_button = QPushButton("IMPORT ACCOUNTS")
        import_accounts_button.setStyleSheet(
            """
            QPushButton {
                background-color: #ffc107;
                color: #ffffff;
                border: none;
                border-radius: 3px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ffa000;
            }
            """
        )

        # Create "EXPORT ACCOUNTS" button
        export_accounts_button = QPushButton("EXPORT ACCOUNTS")
        export_accounts_button.setStyleSheet(
            """
            QPushButton {
                background-color: #ff5722;
                color: #ffffff;
                border: none;
                border-radius: 3px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #f44336;
            }
            """
        )

        # Create a horizontal layout for the table and logs
        table_logs_layout = QHBoxLayout()
        table_logs_layout.addWidget(self.table_widget)

        # Create a vertical layout for the logs box
        logs_layout = QVBoxLayout()
        logs_layout.addWidget(title_label)
        logs_layout.addWidget(logs_scroll_area)

        # Create a widget to hold the logs box
        logs_widget = QWidget()
        logs_widget.setLayout(logs_layout)
        logs_widget.setMinimumHeight(0)  # Set the initial height to zero

        # Create a splitter to adjust the size of the account list and logs
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.table_widget)
        splitter.addWidget(logs_widget)

        # Add the splitter to the layout
        table_logs_layout.addWidget(splitter)

        # Add the table and logs layout to the group box layout
        layout.addLayout(table_logs_layout)

        checkbox_layout = QHBoxLayout()
        checkbox_layout.addWidget(self.check_yt_status_checkbox)
        checkbox_layout.addWidget(self.create_channel_checkbox)


        # Create a vertical layout for the buttons
        buttons_layout = QVBoxLayout()
        buttons_layout.addLayout(checkbox_layout)
        buttons_layout.addWidget(check_accounts_button)
        buttons_layout.addWidget(check_all_button)  # Add the "CHECK ALL NON VERIFIED" button

        # Create a horizontal layout for the import/export buttons
        import_export_layout = QHBoxLayout()
        import_export_layout.addWidget(add_account_button)
        import_export_layout.addWidget(delete_account)
        import_export_layout.addWidget(import_accounts_button)
        import_export_layout.addWidget(export_accounts_button)


        # Add the import/export layout to the buttons layout
        buttons_layout.addLayout(import_export_layout)


        # Add the buttons layout to the group box layout
        layout.addLayout(buttons_layout)

        # Set the group box as the scroll area widget
        scroll_area.setWidget(group_box)

        # Connect the "ADD ACCOUNT" button's clicked signal to a slot
        add_account_button.clicked.connect(self.show_add_account_popup)

        delete_account.clicked.connect(self.delete_account_popup)

        # Connect the "IMPORT ACCOUNTS" button's clicked signal to a slot
        import_accounts_button.clicked.connect(self.show_import_accounts_popup)

        # Connect the "EXPORT ACCOUNTS" button's clicked signal to a slot
        export_accounts_button.clicked.connect(self.show_export_accounts_popup)

        # Connect the "CHECK ACCOUNTS" button's clicked signal to a slot
        check_accounts_button.clicked.connect(self.clicked_check_account)

        # Connect the "CHECK ALL NON VERIFIED" button's clicked signal to a slot
        check_all_button.clicked.connect(self.clicked_check_all_non_verified_accounts)  # Add the appropriate slot method name

        # Connect the "SAVE ALL VERIFIED ACCOUNTS" button's clicked signal to a slot
        save_verified_button.clicked.connect(self.save_all_verified_accounts)

        self.delete_checkbox.stateChanged.connect(self.handle_delete_checkbox_clicked)
        self.notheadless.stateChanged.connect(self.notheadless_handle_checkbox)
        self.check_yt_status_checkbox.stateChanged.connect(self.check_yt_status_checkbox_handle)
        self.create_channel_checkbox.stateChanged.connect(self.create_channel_checkbox_handle)


        self.update_account_list()

        # Create a QTimer to refresh the account list periodically
        refresh_timer = QTimer()
        refresh_timer.timeout.connect(self.refresh_account_list)
        refresh_timer.start(200)  # Adjust the refresh interval (in milliseconds) as needed

    def delete_account_popup(self):
        # Get the selected row in the table widget
        selected_row = self.table_widget.currentRow()
        if selected_row >= 0:
            # Get the Gmail from the selected row
            gmail_item = self.table_widget.item(selected_row, 0)
            if gmail_item is not None:
                gmail = gmail_item.text()

                # Remove the account from the acc.txt file
                lines = []
                with open("data\\accounts.txt", "r") as file:
                    lines = file.readlines()

                if selected_row < len(lines):
                    lines.pop(selected_row)

                with open("data\\accounts.txt", "w") as file:
                    file.writelines(lines)

                self.update_account_list()

                # Remove the row from the table widget
                self.table_widget.removeRow(selected_row)

        self.update_account_list()
    def create_channel_checkbox_handle(self):
        if self.create_channel_checkbox.isChecked():
            # Checkbox is checked
            print("create_channel_checkbox checkbox is checked")
        else:
            # Checkbox is unchecked
            print("create_channel_checkbox checkbox is unchecked")
    def check_yt_status_checkbox_handle(self):
        if self.check_yt_status_checkbox.isChecked():
            # Checkbox is checked
            print("check_yt_status_checkbox checkbox is checked")
        else:
            # Checkbox is unchecked
            print("check_yt_status_checkbox checkbox is unchecked")

    def notheadless_handle_checkbox(self):
        if self.notheadless.isChecked():
            # Checkbox is checked
            print("notheadless checkbox is checked")
        else:
            # Checkbox is unchecked
            print("notheadless checkbox is unchecked")

    def save_all_verified_accounts(self):
        verified_accounts = []

        # Open the "acc.txt" file and read its lines
        with open("data\\accounts.txt", "r") as file:
            lines = file.readlines()

        # Process each line and check for "gmail:pass:yes:yes" format
        for line in lines:
            line = line.strip()
            account_data = line.split(":")
            if len(account_data) == 4 and account_data[2] == "yes" and account_data[3] == "yes":
                gmail = account_data[0]
                password = account_data[1]
                verified_accounts.append({
                    "gmail": gmail,
                    "password": password,
                    "verified": "yes",
                    "yt_status": "no"
                })

        if not verified_accounts:
            # Show a message box notifying the user that no verified accounts were found
            QMessageBox.information(self, "Save Verified Accounts", "No verified accounts found in acccounts.txt.")
            return

        # Check if the "verified_accounts.json" file exists
        if os.path.exists("data\\verified_accounts.json"):
            # Read the existing accounts from the JSON file
            with open("data\\verified_accounts.json", "r") as file:
                try:
                    existing_accounts = json.load(file)
                except json.JSONDecodeError:
                    existing_accounts = []
        else:
            existing_accounts = []

        # Append the new accounts to the existing accounts list
        existing_accounts.extend(verified_accounts)

        # Write the updated accounts back to the JSON file
        with open("data\\verified_accounts.json", "w") as file:
            json.dump(existing_accounts, file, indent=4)

        # Remove the verified accounts from the "acc.txt" file
        lines = [line for line in lines if not line.strip().endswith(":yes:yes")]
        with open("data\\accounts.txt", "w") as file:
            file.writelines(lines)

        # Update the account list in the UI
        self.update_account_list()

        # Show a message box or perform any desired action to notify the user about the successful save
        QMessageBox.information(self, "Save Verified Accounts",
                                "Verified accounts have been saved and removed from accounts.txt.")

    def refresh_account_list(self):
        # Read the contents of the acc.txt file
        db_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data\\accounts.txt")
        lines = []
        with open(db_file, "r") as file:
            lines = file.readlines()

        # Clear the existing rows in the table widget
        self.table_widget.setRowCount(0)

        # Add the updated account data to the table widget
        for line in lines:
            line = line.strip()
            account_data = line.split(":")
            email = account_data[0]
            password = account_data[1]
            verified = account_data[2] if len(account_data) > 2 else 'no'
            yt_status = account_data[3] if len(account_data) > 3 else 'no'

            row_count = self.table_widget.rowCount()
            self.table_widget.insertRow(row_count)
            self.table_widget.setItem(row_count, 0, QTableWidgetItem(email))
            self.table_widget.setItem(row_count, 1, QTableWidgetItem(password))
            self.table_widget.setItem(row_count, 2, QTableWidgetItem(verified))
            self.table_widget.setItem(row_count, 3, QTableWidgetItem(yt_status))

            # Set the cell background color based on the values of 'verified' and 'yt_status'
            if verified.lower() == 'yes':
                self.table_widget.item(row_count, 2).setBackground(QColor('green'))
            elif verified.lower() == 'no':
                self.table_widget.item(row_count, 2).setBackground(QColor('red'))

            if yt_status.lower() == 'yes':
                self.table_widget.item(row_count, 3).setBackground(QColor('green'))
            elif yt_status.lower() == 'no':
                self.table_widget.item(row_count, 3).setBackground(QColor('red'))

        # Resize the columns to fit the content
        self.table_widget.resizeColumnsToContents()

    def handle_delete_checkbox_clicked(self):
        if self.delete_checkbox.isChecked():
            # Checkbox is checked
            print("Delete checkbox is checked")
        else:
            # Checkbox is unchecked
            print("Delete checkbox is unchecked")

    # Store the rows to be processed
    rows_to_process = []

    def clicked_check_all_non_verified_accounts(self):
        # Clear the rows to be processed
        self.rows_to_process = []

        # Iterate through the rows in the table
        for row in range(self.table_widget.rowCount()):
            # Get the "Verified" status of the current row
            verified_item = self.table_widget.item(row, 2)
            if verified_item is None or verified_item.text() != "yes":
                # Get the Gmail and password from the table
                gmail = self.table_widget.item(row, 0).text()
                password = self.table_widget.item(row, 1).text()
                selected_row = row

                # Add the row to the list for processing
                self.rows_to_process.append((gmail, password, selected_row))

        # Start processing the rows
        self.process_next_row()
    def process_next_row(self):
        if len(self.rows_to_process) > 0:
            # Get the next row to process
            gmail_account, gmail_password, selected_row = self.rows_to_process.pop(0)
            # Perform the account checking logic using the gmail and password
            threading.Thread(target=self.check_gmail_account,
                             args=(gmail_account, gmail_password, selected_row)).start()

            # Schedule the next row processing after a delay
            QTimer.singleShot(7000, self.process_next_row)
        else:
            # All rows have been processed
            print("All accounts checked.")

    ##############################################
    # CHECK ACCOUNT BUTTON                       #
    ##############################################

    # Set up logging configuration
    logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(message)s")

    def update_account_list(self):
        # Clear the existing rows in the table
        self.table_widget.setRowCount(0)

        # Read the contents of the accountslist.txt file
        db_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data\\accounts.txt")
        lines = []
        with open(db_file, "r") as file:
            lines = file.readlines()

        # Process each line and populate the table widget
        updated_lines = []
        for line in lines:
            line = line.strip()

            if ":" not in line:
                # Append ":no:no" to the line if it doesn't already exist
                if not line.endswith(":no:no"):
                    line += ":no:no"
            else:
                account_data = line.split(":")
                if len(account_data) == 2:  # If line contains only "gmail:pass"
                    line += ":no:no"

            if ":" in line:
                account_data = line.split(":")
                email = account_data[0]
                password = account_data[1]
                verified = account_data[2] if len(account_data) > 2 else 'no'
                yt_status = account_data[3] if len(account_data) > 3 else 'no'

                # Remove single quotes around 'no'
                verified = verified.strip("'")
                yt_status = yt_status.strip("'")

                # Insert a new row into the table
                row_count = self.table_widget.rowCount()
                self.table_widget.insertRow(row_count)

                # Set the values for each column in the new row
                self.table_widget.setItem(row_count, 0, QTableWidgetItem(email))
                self.table_widget.setItem(row_count, 1, QTableWidgetItem(password))
                self.table_widget.setItem(row_count, 2, QTableWidgetItem(verified))
                self.table_widget.setItem(row_count, 3, QTableWidgetItem(yt_status))

                # Set the cell background color based on the values of 'verified' and 'yt_status'
                if verified.lower() == 'yes':
                    self.table_widget.item(row_count, 2).setBackground(QColor('green'))
                elif verified.lower() == 'no':
                    self.table_widget.item(row_count, 2).setBackground(QColor('red'))

                if yt_status.lower() == 'yes':
                    self.table_widget.item(row_count, 3).setBackground(QColor('green'))
                elif yt_status.lower() == 'no':
                    self.table_widget.item(row_count, 3).setBackground(QColor('red'))

            # Add the updated line to the list
            updated_lines.append(line.strip())

        # Rewrite the updated lines to the accountslist.txt file
        with open(db_file, "w") as file:
            file.write('\n'.join(updated_lines))

    def clicked_check_account(self):

        # Get the selected rows
        selected_rows = set()
        for item in self.table_widget.selectedItems():
            selected_rows.add(item.row())


        print(selected_rows)

        if len(selected_rows) == 1:
            # Get the selected row
            selected_row = list(selected_rows)[0]

            # Get the Gmail and password from the selected row
            gmail = self.table_widget.item(selected_row, 0).text()
            password = self.table_widget.item(selected_row, 1).text()

            # Perform the account checking logic using the Gmail and password
            threading.Thread(target=self.check_gmail_account,
                             args=(gmail, password, selected_row)).start()

    def yt_check_status(self, browser, gmail_account):
        # check if the 'check_yt_status_checkbox' is checked
        if self.check_yt_status_checkbox.isChecked():
            log_message = f"<span style='color:green'>[{gmail_account}] Checking YouTube Account Status...</span>"
            self.logs_text.append(log_message)

            try:
                browser.get('https://www.youtube.com')

                time.sleep(5)

                # Wait for the YouTube page to load
                WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "content")))

                time.sleep(2)

                # Click on the profile avatar
                profile_avatar = browser.find_element(By.XPATH, '//*[@id="img"]')
                profile_avatar.click()

                # Wait for the profile dropdown menu to appear
                WebDriverWait(browser, 10).until(EC.presence_of_element_located(
                    (By.XPATH, '/html/body/ytd-app/ytd-popup-container/tp-yt-iron-dropdown')))

                time.sleep(1)

                channel_link = browser.find_element(By.XPATH,'/html/body/ytd-app/ytd-popup-container/tp-yt-iron-dropdown/div/ytd-multi-page-menu-renderer/div[3]/div[1]/yt-multi-page-menu-section-renderer[1]/div[2]/ytd-compact-link-renderer[1]/a/tp-yt-paper-item/div[2]/yt-formatted-string[1]')
                channel_text = channel_link.text

                if channel_text == "Your channel":
                    log_message = f"<span style='color:green'>[{gmail_account}] YouTube account channel verified!</span>"
                    self.logs_text.append(log_message)

                    # Update the account status in the "acc.txt" file
                    with open("data\\accounts.txt", "r+") as file:
                        lines = file.readlines()
                        file.seek(0)
                        for line in lines:
                            if gmail_account in line:
                                line = line.replace(":no", ":yes")
                            file.write(line)
                        file.truncate()

                    # Update the account list in the UI
                    self.update_account_list()


                elif channel_text == "Create a channel":
                    print("YouTube account status: Not verified (No channel)")
                    log_message = f"<span style='color:red'>[{gmail_account}] YouTube account status: Not verified (No channel)</span>"
                    self.logs_text.append(log_message)

                    try:

                        if self.create_channel_checkbox.isChecked():

                            browser.execute_script("window.open('https://www.spinxo.com/youtube-names');")
                            browser.switch_to.window(browser.window_handles[1])  # Switch to the newly opened tab

                            log_message = f"<span style='color:green'>[{gmail_account}] Autocreating Channel...</span>"
                            self.logs_text.append(log_message)

                            time.sleep(2)

                            # Generate a random channel name
                            generate_button = browser.find_element(By.XPATH, '//*[@id="lnkSpin"]')
                            generate_button.click()

                            time.sleep(7)  # Wait for the name to be generated

                            # Get the generated channel name
                            channel_name_element = browser.find_element(By.XPATH, '//*[@id="divNames0"]/ul/li[2]/a')
                            channel_name = channel_name_element.text + str(random.randint(1, 100))
                            print(f"Name Generated: {channel_name}")

                            log_message = f"<span style='color:green'>[{gmail_account}] name generated: {channel_name}!</span>"
                            self.logs_text.append(log_message)

                            # Switch back to the original YouTube tab
                            browser.switch_to.window(browser.window_handles[0])

                            # Click on 'Create Channel'
                            create_channel_button = browser.find_element(By.XPATH,
                                                                         '/html/body/ytd-app/ytd-popup-container/tp-yt-iron-dropdown/div/ytd-multi-page-menu-renderer/div[3]/div[1]/yt-multi-page-menu-section-renderer[1]/div[2]/ytd-compact-link-renderer[1]/a/tp-yt-paper-item/div[2]/yt-formatted-string[1]')
                            create_channel_button.click()

                            # Wait for the channel creation dialog to appear
                            channel_name_input = WebDriverWait(browser, 10).until(EC.element_to_be_clickable(
                                (By.XPATH,
                                 '/html/body/ytd-app/ytd-popup-container/tp-yt-paper-dialog/ytd-channel-creation-dialog-renderer/div/div[4]/div[1]/tp-yt-paper-input/tp-yt-paper-input-container/div[2]')))

                            time.sleep(5)

                            channel_name_input = browser.execute_script("""
                                                                        var channelNameInput = document.querySelector('input.style-scope.tp-yt-paper-input');
                                                                        channelNameInput.value = arguments[0];
                                                                        return channelNameInput;
                                                                    """, channel_name)

                            # Retrieve the channel name input value
                            channel_name_input_value = channel_name_input.get_attribute("value")
                            print("Channel Name Input Value:", channel_name_input_value)

                            time.sleep(5)

                            # Click on 'Create Channel'
                            create_channel_button = browser.find_element(By.XPATH,
                                                                         '/html/body/ytd-app/ytd-popup-container/tp-yt-paper-dialog/ytd-channel-creation-dialog-renderer/div/div[5]/ytd-button-renderer[2]/yt-button-shape/button/yt-touch-feedback-shape/div/div[2]')
                            create_channel_button.click()

                            time.sleep(10)

                            print(f"YouTube account status: Verified")
                            print(f"Channel Name: {channel_name}")

                            log_message = f"<span style='color:green'>[{gmail_account}] YouTube account channel Created: {channel_name}!</span>"
                            self.logs_text.append(log_message)

                            # Update the account status in the "acc.txt" file
                            with open("data\\accounts.txt", "r+") as file:
                                lines = file.readlines()
                                file.seek(0)
                                for line in lines:
                                    if gmail_account in line:
                                        line = line.replace(":no", ":yes")
                                    file.write(line)
                                file.truncate()

                            # Update the account list in the UI
                            self.update_account_list()

                        else:

                            print("YouTube account status: Not verified (No channel)")

                            log_message = f"<span style='color:red'>[{gmail_account}] YouTube account status: Not verified (No channel)</span>"
                            self.logs_text.append(log_message)

                            # Update the account list in the UI
                            self.update_account_list()
                    except Exception as e:
                        # Handle any exceptions that occur during the process
                        print(f"An error occurred: {str(e)}")




            except Exception as e:
                # Handle any exceptions that occur during the process
                print(f"An error occurred: {str(e)}")


    def check_gmail_account(self, gmail_account, gmail_password, selected_row):

        self.process_next_row()
        # Read the contents of the acc.txt file
        db_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data\\accounts.txt")
        lines = []
        with open(db_file, "r") as file:
            lines = file.readlines()

        # Update the selected row in the table widget with the corresponding line from acc.txt
        if selected_row < len(lines):
            line = lines[selected_row].strip()
            account_data = line.split(":")
            email = account_data[0]
            verified = account_data[2] if len(account_data) > 2 else 'no'
            yt_status = account_data[3] if len(account_data) > 3 else 'no'

            # Update the Gmail, verified, and YouTube status in the table widget
            self.table_widget.setItem(selected_row, 0, QTableWidgetItem(email))
            self.table_widget.setItem(selected_row, 2, QTableWidgetItem(verified))
            self.table_widget.setItem(selected_row, 3, QTableWidgetItem(yt_status))

            # Set the cell background color based on the values of 'verified' and 'yt_status'
            if verified.lower() == 'yes':
                self.table_widget.item(selected_row, 2).setBackground(QColor('green'))
            elif verified.lower() == 'no':
                self.table_widget.item(selected_row, 2).setBackground(QColor('red'))

            if yt_status.lower() == 'yes':
                self.table_widget.item(selected_row, 3).setBackground(QColor('green'))
            elif yt_status.lower() == 'no':
                self.table_widget.item(selected_row, 3).setBackground(QColor('red'))

            options = Options()
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-software-rasterizer")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--enable-profile-password-manager")

            if self.notheadless.isChecked():
                pass
            else:
                options.add_argument("--headless")


            browser = webdriver.Chrome(options=options)

            logs = []  # Store the log messages

            try:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logs.append(f"<span style='color:green'>[{selected_row}] Checking account: {gmail_account}</span>")

                log_message = f"<span style='color:green'>[{selected_row}] Checking account: {gmail_account}</span>"
                self.logs_text.append(log_message)

                browser.get('https://www.gmail.com/')

                email_field = browser.find_element(By.ID, "identifierId")
                email_field.clear()
                email_field.send_keys(gmail_account)

                email_next_button = browser.find_element(By.ID, "identifierNext")
                email_next_button.click()

                password_field = WebDriverWait(browser, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[type="password"]'))
                )
                password_field.clear()
                password_field.send_keys(gmail_password)

                password_next_button = browser.find_element(By.ID, "passwordNext")
                password_next_button.click()



                # Check if the password is invalid
                invalid_password_message = "Wrong password. Try again."
                if invalid_password_message in browser.page_source:
                    logs.append(f"[{gmail_account}] Invalid Password!")
                    log_message = f"<span style='color:red'>[{gmail_account}] Invalid Password!</span>"
                    self.logs_text.append(log_message)

                    # Check if the "DELETE ACCOUNT IF INVALID" checkbox is checked
                    if self.delete_checkbox.isChecked():
                        # Delete the row from the table widget
                        self.table_widget.removeRow(selected_row)
                        logs.append(f"[{gmail_account}] Row deleted due to invalid account.")


                logs.append(f"Opening Gmail login page...")
                log_message = f"<span style='color:green'>[{gmail_account}] Opening Gmail login page...</span>"
                self.logs_text.append(log_message)

                inbox_url = "https://mail.google.com/mail/u/0/#inbox"
                WebDriverWait(browser, 10).until(EC.url_to_be(inbox_url))

                if browser.current_url == inbox_url:
                    logs.append(f"[{gmail_account}] Success Login!")
                    log_message = f"<span style='color:green'>[{gmail_account}] Success Login!</span>"
                    self.logs_text.append(log_message)

                    # Update GUI elements using the main thread
                    self.table_widget.item(selected_row, 0).setBackground(QColor("green"))

                    verified_item = QTableWidgetItem("yes")
                    verified_item.setBackground(QColor("green"))
                    self.table_widget.setItem(selected_row, 2, verified_item)

                    # Update acc.txt file with the updated verification status
                    with open(db_file, "r+") as file:
                        lines = file.readlines()
                        if selected_row < len(lines):
                            line = lines[selected_row].strip()
                            account_data = line.split(":")
                            if len(account_data) > 2:
                                account_data[2] = "yes"  # Update the verification status to 'yes'
                            lines[selected_row] = ":".join(account_data) + "\n"
                            file.seek(0)
                            file.writelines(lines)
                            file.truncate()

                else:

                    # Check if Gmail asks for recovery information and "Not now" button is available
                    recovery_not_now_button = browser.find_element(By.XPATH,
                                                                   "//div[@id='view_container']//button[contains(text(), 'Not now')]")
                    if recovery_not_now_button.is_displayed():
                        recovery_not_now_button.click()
                        logs.append(f"[{gmail_account}] Clicked 'Not now' for recovery options.")
                        log_message = f"<span style='color:green'>[{gmail_account}] Clicked 'Not now' for recovery options.</span>"
                        self.logs_text.append(log_message)


                    logs.append(f"[{gmail_account}] Login Failed!")
                    log_message = f"<span style='color:red'>[{gmail_account}] Login Failed!</span>"
                    self.logs_text.append(log_message)

                    # Check if the password is invalid
                    if invalid_password_message in browser.page_source:
                        logs.append(f"[{gmail_account}] Invalid Password!")
                        log_message = f"<span style='color:red'>[{gmail_account}] Invalid Password!</span>"
                        self.logs_text.append(log_message)

                        # Check if the "DELETE ACCOUNT IF INVALID" checkbox is checked
                        if self.delete_checkbox.isChecked():
                            # Delete the row from the table widget
                            self.table_widget.removeRow(selected_row)
                            logs.append(f"[{gmail_account}] Row deleted due to invalid account.")

                self.yt_check_status(browser, gmail_account)


            except Exception as e:
                error_message = f"Error occurred while checking account!"
                logs.append(error_message)
                log_message = f"<span style='color:red'>[{gmail_account}] {error_message}</span>"
                self.logs_text.append(log_message)
                logs.append(f"[{gmail_account}] Login Failed!")
                log_message = f"<span style='color:red'>[{gmail_account}] Login Failed!</span>"
                self.logs_text.append(log_message)

                # Check if the "DELETE ACCOUNT IF INVALID" checkbox is checked
                if self.delete_checkbox.isChecked():
                    # Delete the row from the table widget
                    self.table_widget.removeRow(selected_row)
                    logs.append(f"[{gmail_account}] Row deleted due to invalid account.")
                    log_message = f"<span style='color:red'>[{gmail_account}] Row deleted due to invalid account!</span>"
                    self.logs_text.append(log_message)

            finally:
                browser.quit()
                # Delay for a certain period to avoid force closing and reduce lag
                time.sleep(2)
    ##############################################
    # EXPORT BUTTON                              #
    ##############################################
    def show_export_accounts_popup(self):
        # Prompt a save file dialog
        file_dialog = QFileDialog()
        file_dialog.setDefaultSuffix("txt")
        file_dialog.setAcceptMode(QFileDialog.AcceptSave)
        file_dialog.setWindowTitle("Export Accounts")
        file_dialog.setNameFilter("Text Files (*.txt)")

        # Set the default file name
        default_file_name = "data\\accounts.txt"
        file_dialog.selectFile(default_file_name)

        # If the user selects a file and confirms the save
        if file_dialog.exec_() == QDialog.Accepted:
            # Get the selected file path
            file_path = file_dialog.selectedFiles()[0]

            try:
                # Open the file in write mode
                with open(file_path, "w") as file:
                    # Write each Gmail account in the format "gmail:password:verified:yt_status"
                    for row in range(self.table_widget.rowCount()):
                        gmail = self.table_widget.item(row, 0).text()
                        password = self.table_widget.item(row, 1).text()
                        verified = self.table_widget.item(row, 2).text()
                        yt_status = self.table_widget.item(row, 3).text()
                        account_info = f"{gmail}:{password}:{verified}:{yt_status}"
                        file.write(account_info + "\n")

                print("Accounts exported successfully.")
            except IOError:
                print("An error occurred while exporting the accounts.")
        else:
            print("Export canceled")
    def show_import_accounts_popup(self):
        # Open a file dialog to select the import file
        file_dialog = QFileDialog()
        file_dialog.setWindowTitle("Import Accounts")
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Text files (*.txt)")
        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            if len(selected_files) > 0:
                file_path = selected_files[0]

                # Clear the table widget before importing new accounts
                self.table_widget.clearContents()
                self.table_widget.setRowCount(0)

                with open(file_path, 'r') as file:
                    lines = file.readlines()

                    # Iterate through each line in the file
                    for line in lines:
                        line = line.strip()
                        account_data = line.split(":")

                        # Check if the line contains the required account information
                        if len(account_data) >= 2:
                            gmail = account_data[0]
                            password = account_data[1]
                            verified = account_data[2] if len(account_data) > 2 else 'no'
                            yt_status = account_data[3] if len(account_data) > 3 else 'no'

                            # Add a new row to the table widget
                            row_count = self.table_widget.rowCount()
                            self.table_widget.insertRow(row_count)

                            # Set the values in the table cells
                            self.table_widget.setItem(row_count, 0, QTableWidgetItem(gmail))
                            self.table_widget.setItem(row_count, 1, QTableWidgetItem(password))
                            self.table_widget.setItem(row_count, 2, QTableWidgetItem(verified))
                            self.table_widget.setItem(row_count, 3, QTableWidgetItem(yt_status))

                            # Set the cell background color based on the values of 'verified' and 'yt_status'
                            if verified.lower() == 'yes':
                                self.table_widget.item(row_count, 2).setBackground(QColor('green'))
                            elif verified.lower() == 'no':
                                self.table_widget.item(row_count, 2).setBackground(QColor('red'))

                            if yt_status.lower() == 'yes':
                                self.table_widget.item(row_count, 3).setBackground(QColor('green'))
                            elif yt_status.lower() == 'no':
                                self.table_widget.item(row_count, 3).setBackground(QColor('red'))
    def add_account_popup_submit_clicked(self):
        gmail = self.gmail_line_edit.text()
        password = self.password_line_edit.text()
        self.add_account(gmail, password)
    def show_add_account_popup(self):

        # Create a dialog for adding an account
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Account")
        dialog.setModal(True)

        # Create layout for the dialog
        layout = QVBoxLayout(dialog)
        layout.addWidget(QLabel("Gmail:"))
        self.gmail_line_edit = QLineEdit()
        layout.addWidget(self.gmail_line_edit)
        layout.addWidget(QLabel("Password:"))
        self.password_line_edit = QLineEdit()
        self.password_line_edit.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_line_edit)

        # Create submit button
        submit_button = QPushButton("Submit")
        layout.addWidget(submit_button)

        # Connect the submit button's clicked signal to the add_account method
        submit_button.clicked.connect(self.add_account_popup_submit_clicked)

        # Show the dialog
        dialog.exec_()
    def add_account(self, gmail, password):
        # Check if the Gmail and password fields are not empty
        if gmail and password:
            # Append the account information to the acc.txt file
            account_data = f"{gmail}:{password}:no:no"
            with open("data\\accounts.txt", "a") as file:
                file.write("\n" + account_data)

            # Add the account to the table widget
            row_count = self.table_widget.rowCount()
            self.table_widget.insertRow(row_count)
            self.table_widget.setItem(row_count, 0, QTableWidgetItem(gmail))
            self.table_widget.setItem(row_count, 1, QTableWidgetItem(password))
            self.table_widget.setItem(row_count, 2, QTableWidgetItem("no"))
            self.table_widget.setItem(row_count, 3, QTableWidgetItem("no"))

            # Clear the input fields in the dialog
            self.gmail_line_edit.clear()
            self.password_line_edit.clear()

            # Show a success message or perform any desired actions

        # Clear the input fields
        self.gmail_line_edit.clear()
        self.password_line_edit.clear()

        self.update_account_list()

    def insert_account_row(self, email, password):
        # Add the account to the table widget
        row_count = self.table_widget.rowCount()
        self.table_widget.insertRow(row_count)

        gmail_item = QTableWidgetItem(email)
        password_item = QTableWidgetItem(password)
        verified_item = QTableWidgetItem("No")
        youtube_status_item = QTableWidgetItem("")

        self.table_widget.setItem(row_count, 0, gmail_item)
        self.table_widget.setItem(row_count, 1, password_item)
        self.table_widget.setItem(row_count, 2, verified_item)
        self.table_widget.setItem(row_count, 3, youtube_status_item)

        # Set the background color of the cell containing "No" to red
        if verified_item.text() == "No":
            verified_item.setBackground(QColor("red"))



    ##############################################
    # MOVE GUI
    ##############################################
    def toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_moving = True
            self.window_position = self.pos() - event.globalPos()
            self.mouse_position = event.globalPos()
    def mouseMoveEvent(self, event):
        if self.is_moving and event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() + self.window_position)
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_moving = False
            self.mouse_position = None
            self.window_position = None

    ##############################################
    # WINDOW BUTTONS
    ##############################################

    def download_image(url, filename):
        response = requests.get(url)
        with open(filename, "wb") as f:
            f.write(response.content)
    def create_window_buttons(self):
        # Create minimize button
        self.minimize_button = QPushButton(self)
        self.minimize_icon_url = "https://cdn.discordapp.com/attachments/973138538017226757/1125073440072810536/minus.png"
        self.minimize_icon_data = requests.get(self.minimize_icon_url).content
        minimize_pixmap = QPixmap()
        minimize_pixmap.loadFromData(self.minimize_icon_data)
        self.minimize_button.setIcon(QIcon(minimize_pixmap))
        self.minimize_button.setFixedSize(30, 30)
        self.minimize_button.setToolTip("Minimize")
        self.minimize_button.setStyleSheet(
            """
            QPushButton {
                background-color: transparent;
                border: none;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 0.1);
            }
            """
        )
        self.minimize_button.clicked.connect(self.showMinimized)

        # Create maximize button
        self.maximize_button = QPushButton(self)
        self.maximize_icon_url = "https://media.discordapp.net/attachments/973138538017226757/1125073439829532712/maximize.png?width=468&height=468"
        self.maximize_icon_data = requests.get(self.maximize_icon_url).content
        maximize_pixmap = QPixmap()
        maximize_pixmap.loadFromData(self.maximize_icon_data)
        self.maximize_button.setIcon(QIcon(maximize_pixmap))
        self.maximize_button.setFixedSize(30, 30)
        self.maximize_button.setToolTip("Maximize")
        self.maximize_button.setStyleSheet(
            """
            QPushButton {
                background-color: transparent;
                border: none;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 0.1);
            }
            """
        )
        self.maximize_button.clicked.connect(self.toggle_maximize)

        # Create close button
        self.close_button = QPushButton(self)
        self.close_icon_url = "https://media.discordapp.net/attachments/973138538017226757/1125073440295100496/delete.png?width=468&height=468"
        self.close_icon_data = requests.get(self.close_icon_url).content
        close_pixmap = QPixmap()
        close_pixmap.loadFromData(self.close_icon_data)
        self.close_button.setIcon(QIcon(close_pixmap))
        self.close_button.setFixedSize(30, 30)
        self.close_button.setToolTip("Close")
        self.close_button.setStyleSheet(
            """
            QPushButton {
                background-color: transparent;
                border: none;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 0.1);
            }
            """
        )
        self.close_button.clicked.connect(self.close)

        # Create the title label
        self.title_label = QLabel("SUB4SUB")
        self.title_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")

        # Create a container widget for the buttons
        buttons_widget = QWidget()
        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setSpacing(0)
        buttons_layout.addWidget(self.minimize_button)
        buttons_layout.addWidget(self.maximize_button)
        buttons_layout.addWidget(self.close_button)
        buttons_widget.setLayout(buttons_layout)

        # Create a container widget for the title bar
        title_bar_widget = QWidget()
        title_bar_widget.setStyleSheet(
            """
            background-color: #ffc100;  /* Cool blue color */
            border-bottom: 1px solid #cccccc;
            """
        )
        title_bar_layout = QHBoxLayout()
        title_bar_layout.setContentsMargins(10, 0, 10, 0)
        title_bar_layout.setSpacing(10)
        title_bar_layout.addWidget(self.title_label, alignment=Qt.AlignLeft)  # Align title to the left
        title_bar_layout.addWidget(buttons_widget, alignment=Qt.AlignRight)
        title_bar_widget.setLayout(title_bar_layout)

        # Set the title bar widget as the window title bar
        self.setMenuWidget(title_bar_widget)

    ##############################################
    # LOG ENTRY
    ##############################################
    def add_log_entry(self, message):
        # Get the current logs text
        logs_text = self.logs_text.toPlainText()

        # Add the new log entry with a newline character
        new_logs_text = f"{logs_text}\n{message}"

        # Set the updated logs text
        self.logs_text.setPlainText(new_logs_text)

        # Scroll to the bottom of the logs
        scroll_bar = self.logs_text.verticalScrollBar()
        scroll_bar.setValue(scroll_bar.maximum())