##############################################
# DASHBOARD TAB                              #
##############################################
import json
import webbrowser
import requests
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtWidgets import QWidget, QGroupBox, QVBoxLayout, QLabel, QPushButton, QHBoxLayout


def add_dashboard_boxes(main_window):
    # Create a parent widget for the dashboard elements
    dashboard_widget = QWidget()

    # Create a layout for the parent widget
    dashboard_layout = QVBoxLayout(dashboard_widget)
    dashboard_layout.setContentsMargins(20, 20, 20, 20)
    dashboard_layout.setSpacing(40)

    # Create a group box for account count and additional features
    account_box = QGroupBox("Verified Account Count (This area is in progress")
    account_layout = QVBoxLayout(account_box)
    # Set the fixed height of the account_box
    account_box.setFixedHeight(400)

    # Create a layout for account count
    account_count_layout = QVBoxLayout()
    account_count_label = QLabel("Total Verified Accounts")
    account_count_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #6b7b8c;")

    # Read the data from the JSON file
    with open("data\\verified_accounts.json") as f:
        verified_accounts_data = json.load(f)

    # Get the total count of verified accounts
    total_verified_accounts = len(verified_accounts_data)

    account_count_value = QLabel(str(total_verified_accounts))
    account_count_value.setStyleSheet("font-size: 32px; font-weight: bold; color: #ef9d10f;")
    account_count_note = QLabel("Note: Only verified accounts counted")
    account_count_note.setStyleSheet("font-size: 10px; color: #6b7b8c;")
    account_count_layout.addWidget(account_count_label, alignment=Qt.AlignCenter)
    account_count_layout.addWidget(account_count_value, alignment=Qt.AlignCenter)
    account_count_layout.addWidget(account_count_note, alignment=Qt.AlignCenter)


    # Add the account count and additional features layouts to the account layout
    account_layout.addLayout(account_count_layout)

    # Add the account box to the dashboard layout and set the stretch factor
    dashboard_layout.addWidget(account_box)
    dashboard_layout.setStretchFactor(account_box, 1)

    def download_image(url, filename):
        response = requests.get(url)
        with open(filename, "wb") as f:
            f.write(response.content)

    top_row_layout = QHBoxLayout()

    # Create a group box for socials
    socials_box = QGroupBox("Socials")
    socials_layout = QHBoxLayout(socials_box)
    socials_box.setMaximumWidth(300)
    socials_box.setFixedHeight(100)
    socials_layout.setAlignment(Qt.AlignCenter)

    # Create YouTube button
    youtube_button = QPushButton()
    youtube_icon_url = "https://media.discordapp.net/attachments/973138538017226757/1125052488534462564/youtube.png?width=665&height=468"
    youtube_icon_data = requests.get(youtube_icon_url).content
    youtube_icon_image = QImage.fromData(youtube_icon_data)
    youtube_button.setIcon(QIcon(QPixmap.fromImage(youtube_icon_image)))
    youtube_button.setStyleSheet("background-color: transparent; border: none;")
    youtube_button.setIconSize(QSize(30, 30))
    youtube_button.setFixedSize(60, 60)

    # Create Discord button
    discord_button = QPushButton()
    discord_icon_url = "https://media.discordapp.net/attachments/973138538017226757/1125052488299593840/discord.png?width=468&height=468"
    discord_icon_data = requests.get(discord_icon_url).content
    discord_icon_image = QImage.fromData(discord_icon_data)
    discord_button.setIcon(QIcon(QPixmap.fromImage(discord_icon_image)))
    discord_button.setStyleSheet("background-color: transparent; border: none;")
    discord_button.setIconSize(QSize(30, 30))
    discord_button.setFixedSize(60, 60)

    # Create Instagram button
    instagram_button = QPushButton()
    instagram_icon_url = "https://media.discordapp.net/attachments/973138538017226757/1125052488773554256/instagram.png?width=468&height=468"
    instagram_icon_data = requests.get(instagram_icon_url).content
    instagram_icon_image = QImage.fromData(instagram_icon_data)
    instagram_button.setIcon(QIcon(QPixmap.fromImage(instagram_icon_image)))
    instagram_button.setStyleSheet("background-color: transparent; border: none;")
    instagram_button.setIconSize(QSize(30, 30))
    instagram_button.setFixedSize(60, 60)

    # Create a horizontal layout for the buttons
    buttons_layout = QHBoxLayout()
    buttons_layout.addWidget(youtube_button)
    buttons_layout.addSpacing(20)
    buttons_layout.addWidget(discord_button)
    buttons_layout.addSpacing(20)
    buttons_layout.addWidget(instagram_button)

    # Add the donate button layout to the donate layout
    socials_layout.addLayout(buttons_layout)

    # Connect the clicked signals of the buttons to open the respective links
    youtube_button.clicked.connect(lambda: webbrowser.open("https://www.youtube.com/channel/UCF-4oYWPvCfaA36RWgFX2rw"))
    discord_button.clicked.connect(lambda: webbrowser.open("https://discord.gg/VwjebvGmm"))
    instagram_button.clicked.connect(lambda: webbrowser.open("https://www.instagram.com/"))



    # Create a group box for donate
    donate_box = QGroupBox("Donate")
    donate_layout = QVBoxLayout(donate_box)
    donate_box.setMaximumWidth(100)
    donate_layout.setAlignment(Qt.AlignCenter)


    # Create Discord button
    crypto_button = QPushButton()
    crypto_icon_url = "https://cdn.discordapp.com/attachments/973138538017226757/1125056777835266168/bitcoin.png"
    crypto_icon_data = requests.get(crypto_icon_url).content
    crypto_icon_image = QImage.fromData(crypto_icon_data)
    crypto_button.setIcon(QIcon(QPixmap.fromImage(crypto_icon_image)))
    crypto_button.setStyleSheet("background-color: transparent; border: none;")
    crypto_button.setIconSize(QSize(30, 30))
    crypto_button.setFixedSize(60, 60)

    # Create a horizontal layout for the donate button
    donate_button_layout = QHBoxLayout()
    donate_button_layout.addStretch()
    donate_button_layout.addWidget(crypto_button)
    donate_button_layout.addStretch()

    # Add the donate button layout to the donate layout
    donate_layout.addLayout(donate_button_layout)

    crypto_button.clicked.connect(lambda: webbrowser.open("https://nowpayments.io/payment/?iid=4776634155&paymentId=4604176834"))

    # Create a group box for account status
    account_status_box = QGroupBox("Account Status")
    account_status_layout = QHBoxLayout(account_status_box)
    account_status_box.setMinimumWidth(200)

    # Create a QLabel for the icon
    icon_label = QLabel()
    icon_url = "https://cdn.discordapp.com/attachments/973138538017226757/1125055127447937125/usericon.png"
    icon_pixmap = QPixmap()
    icon_pixmap.loadFromData(requests.get(icon_url).content)
    icon_label.setPixmap(icon_pixmap)
    icon_label.setFixedSize(30, 30)
    icon_label.setScaledContents(True)

    # Create a QLabel for the account type label
    account_type_label = QLabel("Account type: Free (Beta version)")
    account_type_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #6b7b8c;")

    # Add the icon and account type label to the account status layout
    account_status_layout.addWidget(icon_label)
    account_status_layout.addWidget(account_type_label)

    # Set the alignment of the account status layout to center
    account_status_layout.setAlignment(Qt.AlignCenter)

    # Adjust the alignment of the socials box and account status box within the layout
    top_row_layout.addWidget(socials_box)
    top_row_layout.addWidget(donate_box)
    top_row_layout.addWidget(account_status_box)

    dashboard_layout.addLayout(top_row_layout)


    # Add the group boxes to the dashboard layout
    dashboard_layout.addWidget(account_box)

    # Set the stylesheet for the dashboard widget
    dashboard_widget.setStyleSheet(
        """
        QGroupBox {
            border: 2px solid #6b7b8c;
            border-radius: 5px;
            background-color: #ffffff;
        }

        QLabel {
            font-family: Arial;
        }

        QPushButton {
            border-radius: 3px;
            padding: 5px;
        }
        """
    )

    # Add the dashboard widget to the main layout
    main_window.tab1.layout.addWidget(dashboard_widget)
