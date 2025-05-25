import os
import requests
import zipfile
import wget


def driver_update():
    print("Updating ChromeDriver...")

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
