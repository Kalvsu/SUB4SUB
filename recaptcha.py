import os
import time
import pyautogui
import requests
import speech_recognition as sr
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from pydub import AudioSegment
from selenium.webdriver.chrome import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.devtools.v105.indexed_db import Key
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import createbrowser

def click_checkbox(browser):
    browser.switch_to.default_content()
    browser.switch_to.frame(browser.find_element(By.XPATH, ".//iframe[@title='reCAPTCHA']"))
    checkbox = browser.find_element(By.ID, "recaptcha-anchor-label")
    checkbox.click()
    browser.switch_to.default_content()
    time.sleep(2)


def download_and_save_file(browser, audio_file_path):
    # Wait for the download button to appear
    download_button_xpath = '//*[@id="form-element"]/button'
    wait = WebDriverWait(browser, 20)  # Adjust the timeout value as needed
    download_button = wait.until(EC.visibility_of_element_located((By.XPATH, download_button_xpath)))


    # Get the directory path of the audio file
    audio_file_directory = os.path.dirname(audio_file_path)

    # Switch back to the original tab
    browser.switch_to.window(browser.window_handles[0])
    time.sleep(1)
    browser.switch_to.window(browser.window_handles[1])

    # Click the download button
    browser.execute_script("arguments[0].scrollIntoView();", download_button)
    time.sleep(2)
    download_button.click()

    # Wait for the download prompt to appear
    time.sleep(2)  # Adjust the delay as needed

    # Simulate keyboard inputs to specify the download path and filename
    pyautogui.typewrite(audio_file_directory)
    pyautogui.press('enter')
    time.sleep(0.5)  # Add a small delay

    # Simulate keyboard inputs to set the download filename
    pyautogui.typewrite("downloaded_text_file.txt")
    pyautogui.press('enter')

    # Wait for the download to complete (adjust the timeout value as needed)
    time.sleep(3)

    # Specify the downloaded file path
    downloaded_file_path = os.path.join(audio_file_directory, "downloaded_text_file.txt")

    return downloaded_file_path

def bypass_recaptcha_with_speech(browser):
    wait = WebDriverWait(browser, 20)

    # Create a recognizer instance
    recognizer = sr.Recognizer()

    # Configure the speech recognition settings
    mic = sr.Microphone()
    recaptcha_frame_xpath = "//iframe[@title='reCAPTCHA']"
    recaptcha_audio_challenge_xpath = '//iframe[@id="recaptcha-audio-button"]'

    # Wait for the reCAPTCHA to load
    time.sleep(3)

    # Switch to the reCAPTCHA frame
    recaptcha_frame = browser.find_element(By.XPATH, recaptcha_frame_xpath)
    browser.switch_to.frame(recaptcha_frame)

    # Click the reCAPTCHA checkbox
    click_checkbox(browser)

    # Switch back to the default content
    browser.switch_to.default_content()

    time.sleep(2)

    browser.switch_to.default_content()
    browser.switch_to.frame(
    browser.find_element(By.XPATH, ".//iframe[@title='recaptcha challenge expires in two minutes']"))
    browser.find_element(By.ID, "recaptcha-audio-button").click()

    # Wait for the audio to play
    time.sleep(2)

    # Find and extract the audio source URL
    audio_source = browser.find_element(By.ID, "audio-source").get_attribute('src')

    # Download the audio file
    response = requests.get(audio_source)
    audio_content = response.content

    # Set the audio file path
    audio_file = "audio\\audio.wav"  # Set the desired path here

    # Get the absolute path of the audio file
    audio_file_path = os.path.abspath(audio_file)

    # Save the audio file
    with open(audio_file, "wb") as file:
        file.write(audio_content)

        # Open the website in a new tab
        browser.execute_script("window.open('', '_blank');")
        browser.switch_to.window(browser.window_handles[1])
        browser.get("https://converter.app/wav-to-text/")

    time.sleep(5)

    # Switch back to the original tab
    browser.switch_to.window(browser.window_handles[0])
    time.sleep(1)
    browser.switch_to.window(browser.window_handles[1])

    # Define the XPath for the element with "Click to choose a file" text
    file_input_xpath = '//*[@id="form-element"]/div[2]/label/strong'
    file_input_element = browser.find_element(By.XPATH, file_input_xpath)
    browser.execute_script("arguments[0].scrollIntoView();", file_input_element)
    time.sleep(2)
    wait.until(EC.element_to_be_clickable((By.XPATH, file_input_xpath)))
    file_input_element.click()

    ### download prompt
    # Wait for the file upload dialog prompt to appear
    time.sleep(1)  # Add a small delay to ensure the dialog prompt appears
    pyautogui.write(audio_file_path)  # Type the audio file path into the file dialog prompt
    pyautogui.press('enter')  # Press the Enter key to confirm the file selection

    time.sleep(1)
    downloaded_file_path = download_and_save_file(browser, audio_file_path)
    print("Downloaded file path:", downloaded_file_path)




    # Switch back to the original tab
    browser.switch_to.window(browser.window_handles[0])

    # Retrieve the text from the downloaded text file
    text_file_path = "audio\\downloaded_text_file.txt"  # Set the actual path of the downloaded text file
    with open(text_file_path, "r") as text_file:
        text = text_file.read().strip()

    # Enter the text into the input field
    input_field = browser.find_element(By.ID, "audio-response")
    input_field.send_keys(text)

    # Submit the form
    browser.find_element(By.ID, "recaptcha-verify-button").click()

    # Wait for the result
    time.sleep(5)

    # Close the frame
    browser.switch_to.default_content()

    # Close the audio challenge popup
    audio_popup = browser.find_element(By.XPATH, recaptcha_audio_challenge_xpath)
    browser.switch_to.frame(audio_popup)
    close_button = browser.find_element(By.XPATH, "//button[@title='Close']")
    close_button.click()

    # Switch back to the main frame
    browser.switch_to.default_content()






def test():
    browser = createbrowser.create_browser()
    url = 'https://www.google.com/recaptcha/api2/demo'
    browser.get(url)

    time.sleep(2)
    bypass_recaptcha_with_speech(browser)



test()
