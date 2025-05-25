import json
import os
import re

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, \
    QPushButton, QHBoxLayout, QGroupBox, QTableWidget, QTableWidgetItem, QLineEdit, QMessageBox, QCheckBox

import tabdesign


def set_font_color(item):
    if item.text() == "Yes":
        item.setForeground(QColor(0, 200, 0))  # Set green font color for "Yes"
    elif item.text() == "Pending":
        item.setForeground(QColor(255, 255, 0))  # Set green font color for "Pending"
    elif item.text() == "Success":
        item.setForeground(QColor(0, 200, 0))  # Set green font color for "Success"
    elif item.text() == "Failed":
        item.setForeground(QColor(200, 0, 0))  # Set green font color for "Failed"
    elif item.text() == "Not Active":
        item.setForeground(QColor(200, 0, 0))  # Set green font color for "Failed"
    elif item.text() == "No":
        item.setForeground(QColor(200, 0, 0))  # Set red font color for "No"

def setup_account_list_run(main_window, scroll_area):
    def handle_refresh():
        # Clear the existing account table
        account_table.clearContents()
        account_table.setRowCount(0)

        # Call the setup_account_list_run method to refresh the account list
        setup_account_list_run(main_window, scroll_area)

    def handle_comment_list_clicked():
        comment_list_window = tabdesign.CommentListWindow()
        comment_list_window.exec_()

    # Read the verified accounts from the "verified_accounts.json" file
    verified_accounts = []
    if os.path.exists("data\\verified_accounts.json"):
        with open("data\\verified_accounts.json", "r") as file:
            try:
                verified_accounts = json.load(file)
            except json.JSONDecodeError:
                pass

    # Create a widget for the account list
    account_list_widget = QWidget()

    # Create a layout for the account list widget
    account_list_layout = QVBoxLayout(account_list_widget)
    account_list_layout.setContentsMargins(20, 20, 20, 20)
    account_list_layout.setSpacing(20)

    # Create a group box for the account list
    account_list_box = QGroupBox("VERIFIED LIST")

    # Create a layout for the account list group box
    account_list_box_layout = QVBoxLayout(account_list_box)
    account_list_box_layout.setContentsMargins(0, 0, 0, 0)

    # Create a label to display the account count
    account_count_label = QLabel("Account Count: {}".format(len(verified_accounts)))
    account_count_label.setAlignment(Qt.AlignCenter)
    account_count_label.setStyleSheet("font-size: 14px; font-weight: bold;")

    # Add the account count label to the account list box layout
    account_list_box_layout.addWidget(account_count_label)

    # Create a QTableWidget for the account list
    account_table = QTableWidget()
    account_table.setColumnCount(10)  # Increase column count to accommodate the new columns
    account_table.setHorizontalHeaderLabels(
        ["Select", "Gmail", "Verified", "Subscribe", "Like", "Comment", "Set Comment", "Link Set", "Video Link",
         "Status"])

    # Check if there are any verified accounts
    if verified_accounts:
        # Set the number of rows in the table widget
        account_table.setRowCount(len(verified_accounts))
        # Populate the table widget with account data
        for row, account_data in enumerate(verified_accounts):
            # Create a checkbox item
            checkbox_item = QTableWidgetItem()
            checkbox_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            checkbox_item.setCheckState(Qt.Unchecked)

            # Create table items for other columns
            gmail_item = QTableWidgetItem(account_data.get("gmail", ""))
            verified_item = QTableWidgetItem("Yes" if account_data.get("verified") else "No")
            subscribe_item = QTableWidgetItem("Yes" if account_data.get("subscribe") else "No")
            like_item = QTableWidgetItem("Yes" if account_data.get("like") else "No")
            comment_item = QTableWidgetItem("Yes" if account_data.get("comment") else "No")
            link_set_item = QTableWidgetItem("Yes" if account_data.get("link_set") else "No")
            set_link_item = QTableWidgetItem(account_data.get("video_link", "(Add Video link)"))
            set_comment_item = QTableWidgetItem(account_data.get("setcomment", "(Edit comment)"))
            status_item = QTableWidgetItem("Not Active")

            # Set the items in the respective columns
            account_table.setItem(row, 0, checkbox_item)
            account_table.setItem(row, 1, gmail_item)
            account_table.setItem(row, 2, verified_item)
            account_table.setItem(row, 3, subscribe_item)
            account_table.setItem(row, 4, like_item)
            account_table.setItem(row, 5, comment_item)
            account_table.setItem(row, 6, set_comment_item)
            account_table.setItem(row, 7, link_set_item)
            account_table.setItem(row, 8, set_link_item)
            account_table.setItem(row, 9, status_item)

            # Set font color for Yes/No values
            set_font_color(verified_item)
            set_font_color(subscribe_item)
            set_font_color(like_item)
            set_font_color(comment_item)
            set_font_color(link_set_item)
            set_font_color(status_item)

    # Set the table widget properties
    account_table.setColumnWidth(0, 50)  # Adjust the width of the "Select" column
    account_table.setColumnWidth(6, 80)  # Adjust the width of the "Link Set" column
    account_table.setColumnWidth(7, 80)  # Adjust the width of the "Set Link" column

    # Make all columns uneditable except "Set Comment" and "Video Link"
    for row in range(account_table.rowCount()):
        for col in range(account_table.columnCount()):
            if col != 6 and col != 8:  # Exclude "Set Comment" and "Video Link" columns
                item = account_table.item(row, col)
                if item is not None:
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)

    # Add the table widget to the account list group box layout
    account_list_box_layout.addWidget(account_table)

    # Add the account list group box to the account list layout
    account_list_layout.addWidget(account_list_box)

    # Add the account list widget to the scroll area
    scroll_area.setWidget(account_list_widget)
    scroll_area.setWidgetResizable(True)

    # Resize the table to fit the contents
    account_table.horizontalHeader().setStretchLastSection(True)
    account_table.resizeRowsToContents()
    account_table.setMinimumSize(account_table.horizontalHeader().length() + 5,
                                 account_table.verticalHeader().length() + 5)

    # Add the account table to the account list group box layout
    account_list_box_layout.addWidget(account_table)

    # Add a checkbox for selecting all accounts
    select_all_checkbox = QCheckBox("Select All")
    select_all_checkbox.setStyleSheet("font-size: 14px;")


    # Create a group box for the buttons
    buttons_box = QGroupBox()
    buttons_box.setStyleSheet("QGroupBox { border: 1px solid #a0a0a0; border-radius: 5px; margin-bottom: 20px; }")

    # Create a layout for the buttons group box
    buttons_layout = QVBoxLayout(buttons_box)
    buttons_layout.setContentsMargins(10, 10, 10, 10)
    buttons_layout.setSpacing(10)

    # Create buttons for subscribing, liking, and commenting

    subscribe_button = QPushButton("SET Subscribe")
    like_button = QPushButton("SET Like")
    comment_button = QPushButton("Apply Comment")
    set_link_button = QPushButton("SET Link")
    set_all_button = QPushButton("SET All Action")
    refresh_button = QPushButton("Refresh List")
    comment_list = QPushButton("Comment List")

    # Create a QPushButton for the "CREATE TASK" button
    create_task_button = QPushButton("CREATE TASK")
    create_task_button.setStyleSheet("""
        QPushButton {
            background-color: #00bfff;
            color: #ffffff;
            border: none;
            border-radius: 5px;
            padding: 10px;
            font-weight: bold;
            font-size: 16px;
        }
        QPushButton:hover {
            background-color: #00a0e6;
        }
    """)

    # Add the "CREATE TASK" button at the top of the layout
    buttons_layout.addWidget(create_task_button)

    # Set styles for the buttons
    button_style = """
                QPushButton {
                    background-color: %s;
                    color: #ffffff;
                    border: none;
                    border-radius: 3px;
                    padding: 6px 12px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: %s;
                }
            """

    subscribe_button.setStyleSheet(button_style % ("#ef1010", "#ff2f2f"))
    like_button.setStyleSheet(button_style % ("#1033ef", "#2958ff"))
    comment_button.setStyleSheet(button_style % ("#ffd700", "#ffea00"))
    set_link_button.setStyleSheet(button_style % ("#808080", "#a0a0a0"))
    set_all_button.setStyleSheet(button_style % ("#008000", "#90ee90"))
    refresh_button.setStyleSheet(button_style % ("#000000", "#a0a0a0"))
    comment_list.setStyleSheet(button_style % ("#800080", "#D8BFD8"))

    # Create a horizontal layout for the buttons
    buttons_row_layout = QHBoxLayout()
    buttons_row_layout.addWidget(subscribe_button)
    buttons_row_layout.addWidget(like_button)
    buttons_row_layout.addWidget(comment_button)
    buttons_row_layout.addWidget(set_link_button)
    buttons_row_layout.addWidget(set_all_button)
    buttons_row_layout.addWidget(refresh_button)
    buttons_row_layout.addStretch()

    # Add the buttons row layout to the buttons layout
    buttons_layout.addLayout(buttons_row_layout)

    # Create a layout for the video link section
    link_layout = QHBoxLayout()
    link_textbox = QLineEdit()
    link_textbox.setPlaceholderText("Enter YouTube video link")
    link_layout.addWidget(link_textbox)
    link_layout.addWidget(set_link_button)

    # Add the link layout to the buttons layout
    buttons_layout.addLayout(link_layout)

    # Add the buttons group box to the account list layout
    account_list_layout.addWidget(buttons_box)

    # Create a vertical layout for the buttons and checkbox
    buttons_checkbox_layout = QVBoxLayout()
    buttons_checkbox_layout.addWidget(select_all_checkbox)
    buttons_checkbox_layout.addWidget(comment_list)
    buttons_checkbox_layout.addStretch()
    buttons_checkbox_layout.addWidget(subscribe_button)
    buttons_checkbox_layout.addWidget(like_button)
    buttons_checkbox_layout.addWidget(comment_button)
    buttons_checkbox_layout.addWidget(set_all_button)
    buttons_checkbox_layout.addWidget(link_textbox)
    buttons_checkbox_layout.addWidget(set_link_button)

    # Create a horizontal layout for the buttons and account list
    buttons_account_layout = QHBoxLayout()
    buttons_account_layout.addLayout(buttons_checkbox_layout)
    buttons_account_layout.addWidget(account_list_box)

    # Add the buttons and account list layout to the main layout
    account_list_layout.addLayout(buttons_account_layout)

    # Set the account list widget as the central widget of the scroll area
    scroll_area.setWidget(account_list_widget)
    scroll_area.setWidgetResizable(True)


    refresh_button.clicked.connect(handle_refresh)
    comment_list.clicked.connect(handle_comment_list_clicked)
    subscribe_button.clicked.connect(lambda: handle_subscribe_button_click(account_table, verified_accounts))
    like_button.clicked.connect(lambda: handle_like_button_click(account_table, verified_accounts))
    comment_button.clicked.connect(lambda: handle_comment_button_click(account_table, verified_accounts))
    set_all_button.clicked.connect(lambda: handle_set_all_button_click(account_table, verified_accounts))
    select_all_checkbox.stateChanged.connect(lambda state: select_all_accounts(account_table, state))
    set_link_button.clicked.connect(lambda: set_link_button_clicked(account_table, verified_accounts, link_textbox))

    # Connect the "enable_comment_edit" function to the table widget's itemChanged signal
    account_table.itemChanged.connect(lambda item: enable_comment_edit(item, 6, verified_accounts))
    account_table.itemChanged.connect(lambda item: enable_video_link_edit(item, 8, verified_accounts))

    def update_table_display(table_widget, accounts):
        # Update the table widget with account data
        for row, account_data in enumerate(accounts):
            # Get the table items for the respective columns
            subscribe_item = table_widget.item(row, 3)
            like_item = table_widget.item(row, 4)
            comment_item = table_widget.item(row, 5)
            set_comment_item = table_widget.item(row, 6)  # Added line
            link_set_item = table_widget.item(row, 7)
            video_link_item = table_widget.item(row, 8)



            # Update the text and font color for the respective items based on the account data
            subscribe_item.setText("Yes" if account_data.get("subscribe") else "No")
            like_item.setText("Yes" if account_data.get("like") else "No")
            comment_item.setText("Yes" if account_data.get("comment") else "No")
            link_set_item.setText("Yes" if account_data.get("set_link") else "No")
            video_link_item.setText(account_data.get("video_link", "(Insert videoid)"))
            set_comment_item.setText(account_data.get("setcomment", "(Edit comment)"))  # Added line

            # Set font color for Yes/No values
            set_font_color(subscribe_item)
            set_font_color(like_item)
            set_font_color(comment_item)
            set_font_color(link_set_item)

        # Update the JSON file with the modified account data
        with open("data\\verified_accounts.json", "w") as file:
            json.dump(accounts, file)

        # Refresh the table display
        table_widget.viewport().update()

    def set_link_button_clicked(account_table, verified_accounts, link_textbox):
        link = link_textbox.text()
        at_least_one_selected = False
        if link:
            if "www.youtube.com" not in link:
                QMessageBox.information(None, "Invalid Input", "Please enter a valid YouTube link.")
                return
            # Extract YouTube video ID from the link
            video_id = extract_video_id(link)

            if video_id:

                # Iterate through the rows of the account table
                for row in range(account_table.rowCount()):
                    checkbox_item = account_table.item(row, 0)  # Get the item from the first column

                    # Skip the row if the checkbox item is None or it is not a checkbox item
                    if not checkbox_item or checkbox_item.data(Qt.CheckStateRole) != Qt.Checked:
                        continue

                    at_least_one_selected = True

                    account_data = verified_accounts[row]  # Get the corresponding account data
                    current_set_link = account_data.get("set_link", False)
                    account_data["set_link"] = not current_set_link  # Toggle the "set_link" value

                    current_video_id = account_data.get("video_link")
                    if current_video_id == video_id:  # If the current video ID is equal to the new video ID
                        account_data["video_link"] = ""  # Set the "video_link" field to an empty string
                    else:
                        account_data["video_link"] = video_id  # Update the "video_link" field with the new video ID

                # If no checkbox is selected, show a message box
                if not at_least_one_selected:
                    QMessageBox.information(None, "No Selection", "Please select at least one account.")

                # Save the updated verified_accounts data to "verified_accounts.json"
                with open("data\\verified_accounts.json", "w") as file:
                    json.dump(verified_accounts, file)

        else:
            QMessageBox.information(None, "Error", "Invalid YouTube link.")

        update_table_display(account_table, verified_accounts)

    def extract_video_id(link):
        # Extract the video ID from the YouTube link
        # This implementation assumes that the video ID is the last part of the URL after the "v=" parameter
        video_id = link.split("v=")[-1]
        return video_id

    def handle_subscribe_button_click(account_table, verified_accounts):
        at_least_one_selected = False

        # Iterate through the rows of the account table
        for row in range(account_table.rowCount()):
            checkbox_item = account_table.item(row, 0)  # Get the item from the first column

            # Skip the row if the checkbox item is None or it is not a checkbox item
            if not checkbox_item or checkbox_item.data(Qt.CheckStateRole) != Qt.Checked:
                continue

            at_least_one_selected = True

            account_data = verified_accounts[row]  # Get the corresponding account data
            current_subscribe_value = account_data.get("subscribe", False)
            account_data["subscribe"] = not current_subscribe_value  # Toggle the like value

        # If no checkbox is selected, show a message box
        if not at_least_one_selected:
            QMessageBox.information(None, "No Selection", "Please select at least one account.")

        # Write the updated data back to the JSON file
        with open("data\\verified_accounts.json", "w") as file:
            json.dump(verified_accounts, file)

        update_table_display(account_table, verified_accounts)

    def handle_like_button_click(account_table, verified_accounts):
        # Flag to track if at least one checkbox is selected
        at_least_one_selected = False

        # Iterate through the rows of the account table
        for row in range(account_table.rowCount()):
            checkbox_item = account_table.item(row, 0)  # Get the item from the first column

            # Skip the row if the checkbox item is None or it is not a checkbox item
            if not checkbox_item or checkbox_item.data(Qt.CheckStateRole) != Qt.Checked:
                continue

            at_least_one_selected = True

            account_data = verified_accounts[row]  # Get the corresponding account data
            current_like_value = account_data.get("like", False)
            account_data["like"] = not current_like_value  # Toggle the like value

        # If no checkbox is selected, show a message box
        if not at_least_one_selected:
            QMessageBox.information(None, "No Selection", "Please select at least one account.")

        # Write the updated data back to the JSON file
        with open("data\\verified_accounts.json", "w") as file:
            json.dump(verified_accounts, file)

        update_table_display(account_table, verified_accounts)

    def handle_comment_button_click(account_table, verified_accounts):
        # Read the comments from the "comments.txt" file
        comments = []
        if os.path.exists("data\\comments.txt"):
            with open("data\\comments.txt", "r") as file:
                comments = file.readlines()

        if comments:
            at_least_one_selected = False

            # Iterate through the rows of the account table
            for row in range(account_table.rowCount()):
                checkbox_item = account_table.item(row, 0)  # Get the item from the first column

                # Skip the row if the checkbox item is None or it is not a checkbox item
                if not checkbox_item or checkbox_item.data(Qt.CheckStateRole) != Qt.Checked:
                    continue

                at_least_one_selected = True

                account_data = verified_accounts[row]  # Get the corresponding account data
                current_comment_value = account_data.get("comment", "No")  # Set default value as "No"
                account_data["comment"] = not current_comment_value  # Toggle the comment value

                # Update the verified_accounts data with the comment
                if account_data["comment"]:
                    if row < len(comments):
                        account_data["setcomment"] = comments[row].strip()  # Set the comment from comments.txt
                    else:
                        account_data["setcomment"] = ""  # Set empty string if no comment found
                else:
                    account_data["setcomment"] = ""  # Set empty string when comment is toggled off

            # If no checkbox is selected, show a message box
            if not at_least_one_selected:
                QMessageBox.information(None, "No Selection", "Please select at least one account.")

            # Write the updated data back to the JSON file
            with open("data\\verified_accounts.json", "w") as file:
                json.dump(verified_accounts, file)

            update_table_display(account_table, verified_accounts)

        else:
            # No comments available, show a message
            QMessageBox.information(None, "No Comments", "No comments available in the comment list.")

    def handle_set_all_button_click(account_table, verified_accounts):
        # Read the comments from the "comments.txt" file
        comments = []
        if os.path.exists("data\\comments.txt"):
            with open("data\\comments.txt", "r") as file:
                comments = file.readlines()

        if comments:
            # Flag to track if at least one checkbox is selected
            at_least_one_selected = False

            # Iterate through the rows of the account table
            for row in range(account_table.rowCount()):
                checkbox_item = account_table.item(row, 0)  # Get the item from the first column

                # Skip the row if the checkbox item is None or it is not a checkbox item
                if not checkbox_item or checkbox_item.data(Qt.CheckStateRole) != Qt.Checked:
                    continue

                at_least_one_selected = True

                account_data = verified_accounts[row]  # Get the corresponding account data
                current_subscribe_value = account_data.get("subscribe", False)
                account_data["subscribe"] = not current_subscribe_value  # Toggle the subscribe value

                account_data = verified_accounts[row]  # Get the corresponding account data
                current_like_value = account_data.get("like", False)
                account_data["like"] = not current_like_value  # Toggle the like value

                account_data = verified_accounts[row]  # Get the corresponding account data
                current_comment_value = account_data.get("comment", False)  # Set default value as "No"
                account_data["comment"] = not current_comment_value  # Toggle the comment value

                # Update the verified_accounts data with the comment
                if account_data["comment"]:
                    if row < len(comments):
                        account_data["setcomment"] = comments[row].strip()  # Set the comment from comments.txt
                    else:
                        account_data["setcomment"] = ""  # Set empty string if no comment found
                else:
                    account_data["setcomment"] = ""  # Set empty string when comment is toggled off

            # If no checkbox is selected, show a message box
            if not at_least_one_selected:
                QMessageBox.information(None, "No Selection", "Please select at least one account.")

            # Write the updated data back to the JSON file
            with open("data\\verified_accounts.json", "w") as file:
                json.dump(verified_accounts, file)

            update_table_display(account_table, verified_accounts)
        else:
            # No comments available, show a message
            QMessageBox.information(None, "No Comments", "No comments available in the comment list.")

    def enable_comment_edit(item, column, verified_accounts):
        if item.column() == column:
            row = item.row()
            account_data = verified_accounts[row]  # Get the corresponding account data

            # Update the "setcomment" field in the account data
            new_comment = item.text()
            account_data["setcomment"] = new_comment

            # Save the updated verified_accounts data to "verified_accounts.json"
            with open("data\\verified_accounts.json", "w") as file:
                json.dump(verified_accounts, file, indent=4)  # Indent for better readability

    def enable_video_link_edit(item, column, verified_accounts):
        if item.column() == column:
            row = item.row()
            account_data = verified_accounts[row]  # Get the corresponding account data

            # Update the "video_link" field in the account data
            new_video_link = item.text()
            account_data["video_link"] = new_video_link

            # Save the updated verified_accounts data to "verified_accounts.json"
            with open("data\\verified_accounts.json", "w") as file:
                json.dump(verified_accounts, file, indent=4)  # Indent for better readability


    def select_all_accounts(table_widget, state):
        for row in range(table_widget.rowCount()):
            item = table_widget.item(row, 0)
            if item is not None:
                item.setCheckState(Qt.Checked if state == Qt.Checked else Qt.Unchecked)