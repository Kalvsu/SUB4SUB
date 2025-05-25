from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def create_browser():
    # Create Chrome options
    options = Options()
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--enable-profile-password-manager")
    options.add_argument("--disable-popup-blocking")  # Disable popup blocking
    options.add_argument("--dns-prefetch-disable")  # Disable DNS prefetching
    options.add_argument("--no-sandbox")  # Disable sandbox mode for increased speed
    options.add_argument("--disable-notifications")  # Disable notifications
    options.add_argument("--disable-geolocation")  # Disable geolocation services
    options.add_argument("--disable-infobars")  # Disable the "Chrome is being controlled by automated test software" infobar
    options.add_argument("--disable-web-security")  # Disable web security to speed up loading on some pages (not recommended for regular browsing)
    options.add_argument("--prompt-for-download")  # Always prompt for download location

    # Set user-agent to a mobile device to potentially load mobile versions of websites (optional)
    options.add_argument(
        "user-agent=Mozilla/5.0 (Linux; Android 10; SM-G970F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Mobile Safari/537.36"
    )


    browser = webdriver.Chrome(options=options)

    return browser
