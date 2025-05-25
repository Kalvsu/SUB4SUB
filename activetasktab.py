import json
import os
import threading
import time
from datetime import datetime
from PyQt5.QtGui import QColor, QBrush, QFont, QPixmap
from PyQt5.QtWidgets import QVBoxLayout, QLabel, \
    QPushButton, QHBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QFrame, QTextEdit

from selenium.webdriver.chrome import webdriver
from selenium.webdriver.chrome.options import Options
from selenium import webdriver


import tasker

# Add these variables to the top of the script to keep track of the sent counts
sent_sub_count = 0
sent_like_count = 0
sent_comment_count = 0




def setup_active_task(main_window):

    # Create a QPlainTextEdit for displaying the logs
    logs_text_edit = QTextEdit()
    logs_text_edit.setStyleSheet(
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
    logs_text_edit.setReadOnly(True)

    # Apply bold style to the logs text
    logs_font = QFont()
    logs_font.setBold(True)
    logs_text_edit.setFont(logs_font)

    # Create a QFrame for the active task logs
    logs_frame = QFrame()
    logs_frame_layout = QVBoxLayout(logs_frame)

    # Create a QLabel for the logs frame title bar
    logs_frame_title = QLabel("Active Task Logs")
    logs_frame_title.setStyleSheet("font-weight: bold; font-size: 14px; color: #FFFFFF; background-color: #007BFF; padding: 8px;")
    logs_frame_layout.addWidget(logs_frame_title)

    logs_frame_layout.addWidget(logs_text_edit)
    logs_frame.setStyleSheet("QFrame { background-color: #EFEFEF; border-radius: 10px; }")

    # Create a QFrame for the active instances
    active_instances_frame = QFrame()
    active_instances_frame_layout = QVBoxLayout(active_instances_frame)

    # Create a QLabel for the active instances frame title bar
    active_instances_frame_title = QLabel("Active Instances")
    active_instances_frame_title.setStyleSheet(
        "font-weight: bold; font-size: 14px; color: #FFFFFF; background-color: #007BFF; padding: 8px;")
    active_instances_frame_layout.addWidget(active_instances_frame_title)

    # Create the QTableWidget
    excel_table = QTableWidget()

    # Set the table properties
    excel_table.setColumnCount(3)  # Set the number of columns
    excel_table.setHorizontalHeaderLabels(["GMAIL", "STATUS", "VIDEO LINK"])  # Set column labels

    # Set the resize mode for the columns to fit the widget
    excel_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


    # Add the table to the active instances frame
    active_instances_frame_layout.addWidget(excel_table)


    def add_log(log_message):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logs_text_edit.append(f"<span style='color:green'>[{current_time}]</span> {log_message}")

    def auto_video_active_wrapper(gmail, password, video_link, log_function, row_data, active_instances_data, status_item, excel_table, current_row):
        # Create the browser instance and perform actions
        options = Options()
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--enable-profile-password-manager")
        options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        options.add_experimental_option('useAutomationExtension', False)
        prefs = {
            "intl.accept_languages": 'en_US,en',
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.default_content_setting_values.notifications": 2,
            "download_restrictions": 3
        }
        options.add_experimental_option("prefs", prefs)

        browser = webdriver.Chrome(options=options)

        # Create a separate thread for the actual auto_video_active function
        def auto_video_active_thread(keep_running):
            # Check if the browser is still open and the thread should continue running
            while keep_running and browser.window_handles:
                try:
                    # Perform the auto_video_active actions
                    tasker.auto_video_active(gmail, password, video_link, log_function, browser, row_data, active_instances_data, status_item, excel_table, current_row)
                except Exception as e:
                    # Handle any exceptions that occur during auto_video_active
                    print(f"An error occurred: {str(e)}")

            # Close the browser if it is still open
            if browser.window_handles:
                browser.quit()

        # Start the thread
        keep_running = True
        thread = threading.Thread(target=auto_video_active_thread, args=(keep_running,), daemon=True)
        thread.start()

        # Return the thread object
        return thread

    def stop_thread(thread):
        # Set the flag to stop the thread
        thread.keep_running = False




    def refresh_active_instances():
        # Read the verified accounts from the "verified_accounts.json" file
        active_instances_data = []
        if os.path.exists("data\\active_instances.json"):
            with open("data\\active_instances.json", "r") as file:
                try:
                    active_instances_data = json.load(file)
                except json.JSONDecodeError:
                    pass

        # Clear the existing rows in the excel_table
        excel_table.setRowCount(0)

        # Add data to the excel_table and update counts
        for row_data in active_instances_data:
            gmail = row_data.get("gmail", "")
            password = row_data.get("password")
            status = row_data.get("status", "Pending")
            video_link = row_data.get("video_link", "")

            # Get the current row count
            current_row = excel_table.rowCount()

            # Insert a new row
            excel_table.insertRow(current_row)

            # Set data in the cells
            gmail_item = QTableWidgetItem(gmail)
            status_item = QTableWidgetItem(status)
            video_link_item = QTableWidgetItem(video_link)

            excel_table.setItem(current_row, 0, gmail_item)
            excel_table.setItem(current_row, 1, status_item)
            excel_table.setItem(current_row, 2, video_link_item)

            set_font_color(status_item)

            # Run auto_like_video if gmail, password, and video_link exist
            if gmail and password and video_link:
                if status == "All Actions Completed":
                    status = "Pending"
                    status_item = QTableWidgetItem(status)
                    excel_table.setItem(current_row, 1, status_item)
                    set_font_color(status_item)

                    # Update the status to "Pending" in the active_instances_data
                    row_data["status"] = "Pending"

                    # Save the updated active_instances_data to the "active_instances.json" file
                    with open("data\\active_instances.json", "w") as file:
                        json.dump(active_instances_data, file, indent=4)

                    # Update the status to "All Actions Completed" in the GUI
                    status_item = QTableWidgetItem("Pending")
                    excel_table.setItem(current_row, 1, status_item)
                    set_font_color(status_item)

                    video_thread = auto_video_active_wrapper(gmail, password, video_link, add_log, row_data,
                                                             active_instances_data, status_item, excel_table,
                                                             current_row)
                    log_message = f"[{gmail}] Thread Initiated! "
                    add_log(log_message)
                    time.sleep(10)

                    # Stop the thread and close the browser
                    stop_thread(video_thread)

                elif status == "Gmail requires verification":
                    log_message = f"<span style='color:blue'>[{gmail}]</span> <span style='color:red'> Skipped! Gmail requires verification.</span>"
                    add_log(log_message)

                    # Update the status to "All Actions Completed" in the GUI
                    status_item = QTableWidgetItem("Gmail requires verification")
                    excel_table.setItem(current_row, 1, status_item)
                    set_font_color(status_item)

                else:
                    status = "Pending"
                    status_item = QTableWidgetItem(status)
                    excel_table.setItem(current_row, 1, status_item)
                    set_font_color(status_item)

                    # Update the status to "Pending" in the active_instances_data
                    row_data["status"] = "Pending"

                    # Save the updated active_instances_data to the "active_instances.json" file
                    with open("data\\active_instances.json", "w") as file:
                        json.dump(active_instances_data, file, indent=4)

                    # Update the status to "All Actions Completed" in the GUI
                    status_item = QTableWidgetItem("Pending")
                    excel_table.setItem(current_row, 1, status_item)
                    set_font_color(status_item)

                    video_thread = auto_video_active_wrapper(gmail, password, video_link, add_log, row_data,
                                                             active_instances_data, status_item, excel_table,
                                                             current_row)
                    log_message = f"[{gmail}] Thread Initiated! "
                    add_log(log_message)
                    time.sleep(10)

                    # Stop the thread and close the browser
                    stop_thread(video_thread)







        # Refresh the GUI
        main_window.tab4.update()




    # Create a QHBoxLayout to contain the active logs frame and active instances frame
    main_content_layout = QHBoxLayout()
    main_content_layout.addWidget(logs_frame)
    main_content_layout.addWidget(active_instances_frame)

    # Create a QVBoxLayout for the main content



    # Create the Load button
    load_button = QPushButton("Load Verified Accounts/Run Created Task")

    # Set the button's style sheet
    load_button.setStyleSheet(
        """
        QPushButton {
            background-color: #007BFF;
            border-radius: 10px;
            padding: 8px;
            font-weight: bold;
            font-size: 12px;
            color: white;
        }

        QPushButton:hover {
            background-color: #ADD8E6;
        }

        QPushButton:pressed {
            background-color: #5F9EA0;
        }
        """
    )

    main_layout = QVBoxLayout()
    main_layout.addWidget(load_button)
    main_layout.addLayout(main_content_layout)

    # Create a QFrame for the main content
    main_frame = QFrame()
    main_frame.setLayout(main_layout)
    main_frame.setStyleSheet(
        "QFrame { background-color: #EFEFEF; border-radius: 10px; }"
    )

    # Assign the main frame as the central widget of main_window.tab4
    main_window.tab4.scroll_area.setWidget(main_frame)

    # Add a custom background image to the tab
    main_window.tab4.setAutoFillBackground(True)
    palette = main_window.tab4.palette()
    palette.setBrush(main_window.tab4.backgroundRole(), QBrush(QPixmap("background_image.png")))
    main_window.tab4.setPalette(palette)

    # Refresh the GUI
    main_window.tab4.update()

    load_button.clicked.connect(lambda: load_data(refresh_active_instances))

def load_data(refresh_active_instances):
    # Implement the code to load data here

    # Create a separate thread for loading and updating data
    def load_data_thread():
        # Load the data
        # ...

        # Update the GUI
        refresh_active_instances()

    # Create the thread and start it
    thread = threading.Thread(target=load_data_thread, daemon=True)
    thread.start()











def set_font_color(item):
    if item.text() == "Yes":
        item.setForeground(QColor(0, 200, 0))  # Set green font color for "Yes"
    elif item.text() == "Pending":
        item.setForeground(QColor(0, 130, 240)) # Set green font color for "Pending"
    elif item.text() == "All Actions Completed":
        item.setForeground(QColor(0, 200, 0)) # Set green font color for "Success"
    elif item.text() == "Gmail requires verification":
        item.setForeground(QColor(200, 0, 0))  # Set red font color for "No
    elif item.text() == "Failed":
        item.setForeground(QColor(200, 0, 0)) # Set green font color for "Failed"
    elif item.text() == "Not Active":
        item.setForeground(QColor(200, 0, 0))  # Set green font color for "Failed"
    elif item.text() == "No":
        item.setForeground(QColor(200, 0, 0))  # Set red font color for "No"


