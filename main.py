from PyQt5.QtWidgets import QApplication
import os
import requests
import zipfile
import wget
import mainwindow
import sys
import json


def create_config_file():
    default_config = {
        "auto_update_driver": False
    }

    with open("config.json", "w") as config_file:
        json.dump(default_config, config_file, indent=4)


def driver_update():
    print("Updating ChromeDriver...")

    # Check if config.json file exists
    if not os.path.isfile("config.json"):
        create_config_file()

    # Read the config.json file
    with open("config.json") as config_file:
        config = json.load(config_file)

    # Check the value of auto_update_driver
    if config.get("auto_update_driver", True):
        # Get the latest ChromeDriver version number
        url = 'https://chromedriver.storage.googleapis.com/LATEST_RELEASE'
        response = requests.get(url)
        version_number = response.text

        # Build the download URL
        download_url = "https://chromedriver.storage.googleapis.com/" + version_number + "/chromedriver_win32.zip"

        # Download the zip file using the URL built above
        latest_driver_zip = wget.download(download_url, 'chromedriver.zip')

        # Set the destination path to the current directory
        destination_path = os.getcwd()

        # Extract the zip file to the destination path
        with zipfile.ZipFile(latest_driver_zip, 'r') as zip_ref:
            zip_ref.extractall(destination_path)

        # Delete the LICENSE.chromedriver file
        license_file_path = os.path.join(destination_path, "LICENSE.chromedriver")
        if os.path.exists(license_file_path):
            os.remove(license_file_path)

        # Delete the zip file downloaded above
        os.remove(latest_driver_zip)

        # Return the path to the extracted driver
        driver_path = os.path.join(destination_path, "chromedriver.exe")

        print("Drivers updated!")
        return driver_path
    else:
        # Return the path to the existing driver
        driver_path = os.path.join(os.getcwd(), "chromedriver.exe")
        return driver_path


driver_update()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = mainwindow.MainWindow()
    window.show()
    sys.exit(app.exec())
