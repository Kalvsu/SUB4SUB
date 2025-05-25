import json
import os
import time
import traceback
from random import shuffle

import requests
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QTableWidgetItem
from selenium.common import WebDriverException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import warnings


ytbutton_elements_location_dict = {
    "yt_id_like_button": "segmented-like-button",
    "yt_id_sub_button_type1": "subscribe-button",
    "yt_css_like_button_active": "#top-level-buttons-computed > "
                                 "ytd-toggle-button-renderer.style-scope.ytd-menu-renderer.force-icon-button.style"
                                 "-default-active",
    "yt_css_sub_button": "#subscribe-button > ytd-subscribe-button-renderer > tp-yt-paper-button",
    "yt_js_like_button": "document.querySelector('#top-level-buttons-computed >"
                         " ytd-toggle-button-renderer:nth-child(1)').click()",
    "yt_js_sub_button": 'document.querySelector("#subscribe-button >'
                        ' ytd-subscribe-button-renderer > tp-yt-paper-button").click()',

}


def bypass_other_popup(driver):
    popups = ['Got it', 'Skip trial', 'No thanks', 'Dismiss', 'Not now']
    shuffle(popups)

    for popup in popups:
        try:
            driver.find_element(
                By.XPATH, f"//*[@id='button' and @aria-label='{popup}']").click()
        except WebDriverException:
            pass

    try:
        driver.find_element(
            By.XPATH, '//*[@id="dismiss-button"]/yt-button-shape/button').click()
    except WebDriverException:
        pass


def set_font_color(item):
    if item.text() == "Yes":
        item.setForeground(QColor(0, 200, 0))  # Set green font color for "Yes"
    elif item.text() == "Pending":
        item.setForeground(QColor(0, 130, 240))  # Set green font color for "Pending"
    elif item.text() == "All Actions Completed":
        item.setForeground(QColor(0, 200, 0))  # Set green font color for "Success"
    elif item.text() == "Failed":
        item.setForeground(QColor(200, 0, 0))  # Set green font color for "Failed"
    elif item.text() == "Not Active":
        item.setForeground(QColor(200, 0, 0))  # Set green font color for "Failed"
    elif item.text() == "Gmail requires verification":
        item.setForeground(QColor(200, 0, 0))  # Set red font color for "No
    elif item.text() == "Subscribing":
        item.setForeground(QColor(0, 200, 0))  # Set green font color for "Subsribing"
    elif item.text() == "Liking":
        item.setForeground(QColor(0, 200, 0))  # Set green font color for "Liking"
    elif item.text() == "Commenting":
        item.setForeground(QColor(0, 200, 0))  # Set green font color for "Commenting"


def dump_status_update(row_data, active_instances_data, status, excel_table, current_row, browser):
    # Update the status to "All Actions Completed"
    row_data["status"] = status

    # Save the updated active_instances_data to the "active_instances.json" file
    with open("data\\active_instances.json", "w") as file:
        json.dump(active_instances_data, file, indent=4)

    # Update the status to "All Actions Completed" in the GUI
    status_item = QTableWidgetItem(status)
    excel_table.setItem(current_row, 1, status_item)
    set_font_color(status_item)





def auto_video_active(gmail_account, gmail_password, video_id, log_function, browser, row_data, active_instances_data, status_item, excel_table, current_row):


    wait = WebDriverWait(browser, 20)


    try:
        json_data = []  # Initialize json_data variable

        if os.path.exists("data\\active_instances.json"):
            with open("data\\active_instances.json", "r") as file:
                try:
                    json_data = json.load(file)
                except json.JSONDecodeError:
                    pass

        url = 'https://www.gmail.com/'
        browser.get(url)

        log_message = f"<span style='color:blue'>[{gmail_account}]</span> <span style='color:green'> Logging in...</span>"
        log_function(log_message)

        time.sleep(2)


        email_field = browser.find_element(By.ID, "identifierId")
        email_field.clear()
        email_field.send_keys(gmail_account)

        email_next_button = browser.find_element(By.ID, "identifierNext")
        email_next_button.click()

        bypass_other_popup(browser)  # Handle popups
        time.sleep(2)

        password_field = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[type="password"]'))
        )
        password_field.clear()
        password_field.send_keys(gmail_password)

        password_next_button = browser.find_element(By.ID, "passwordNext")
        password_next_button.click()

        bypass_other_popup(browser)  # Handle popups

        time.sleep(2)

        if "accounts.google.com/signin/v2/challenge" in browser.current_url:
            # Gmail asks for verification, log the message and quit the browser
            log_message = f"<span style='color:blue'>[{gmail_account}]</span> <span style='color:red'> Gmail requires verification. Ending session.</span>"
            log_function(log_message)


            dump_status_update(row_data, active_instances_data, "Gmail requires verification", excel_table, current_row, browser)
            return



        if "https://accounts.google.com/speedbump/idvreenable" in browser.current_url:
            # Gmail asks for verification, log the message and quit the browser
            log_message = f"<span style='color:blue'>[{gmail_account}]</span> <span style='color:red'> Gmail requires verification. Ending session.</span>"
            log_function(log_message)


            dump_status_update(row_data, active_instances_data, "Gmail requires verification", excel_table, current_row, browser)
            return

        time.sleep(2)


        url = 'https://youtube.com/watch?v=' + video_id
        browser.get(url)

        log_message = f"<span style='color:blue'>[{gmail_account}]</span> <span style='color:green'> Going to Youtube.com...</span>"
        log_function(log_message)


        time.sleep(5)  # Adjust the sleep time if necessary

        try:
            while True:
                # Check if the ad skip button is present
                ad_skip_button = browser.find_elements(By.CLASS_NAME, 'ytp-ad-skip-button-text')
                if ad_skip_button:
                    # Wait until the ad skip button is visible
                    WebDriverWait(browser, 10).until(EC.visibility_of(ad_skip_button[0]))

                    # Click the ad skip button
                    ad_skip_button[0].click()
                    print("Clicked Skip Ads")

                    log_message = f"<span style='color:blue'>[{gmail_account}]</span> <span style='color:green'> Skipped ads!</span>"
                    log_function(log_message)

                # Check if the video is playing
                video_playing = browser.find_element(By.CLASS_NAME, 'ytp-play-button').get_attribute('aria-label')
                if video_playing == 'Pause':
                    break  # Exit the loop when the video is playing after ads

                break  # Exit the loop when there are no more ads

            time.sleep(5)

        except NoSuchElementException:
            # Error occurred, or ad skip button not found
            print("Error occurred or ad skip button not found")

            log_message = f"<span style='color:blue'>[{gmail_account}]</span> <span style='color:green'> Error occurred or ad skip button not found!</span>"
            log_function(log_message)

        except NameError:
            # total_duration variable not defined
            print("total_duration variable not defined")

            log_message = f"<span style='color:blue'>[{gmail_account}]</span> <span style='color:green'> total_duration variable not defined!</span>"
            log_function(log_message)

        except (WebDriverException, StaleElementReferenceException):
            # Browser window closed or not accessible
            print("Browser window closed or not accessible")

            log_message = f"<span style='color:blue'>[{gmail_account}]</span> <span style='color:green'> Browser window closed or not accessible!</span>"
            log_function(log_message)

        except:
            # Other unexpected errors
            print("An unexpected error occurred")

            log_message = f"<span style='color:blue'>[{gmail_account}]</span> <span style='color:green'> An unexpected error occurred!</span>"
            log_function(log_message)

        time.sleep(5)

        for whatdata in json_data:
            if whatdata.get("subscribe"):

                dump_status_update(row_data, active_instances_data, "Subscribing", excel_table, current_row, browser)


                subscribed = False  # Initialize variable to track subscription status
                try:
                    subscribed_element = browser.find_element(By.CSS_SELECTOR,
                                                              '#notification-preference-button > ytd-subscription-notification-toggle-button-renderer-next > yt-button-shape > button > yt-touch-feedback-shape > div')
                    subscribed = subscribed_element.get_attribute('aria-pressed')
                except NoSuchElementException:
                    pass

                if not subscribed:  # Only subscribe if not already subscribed
                    while True:
                        try:
                            print("clicking sub")
                            subscribe_button = browser.find_element(By.XPATH,
                                                                    '//*[@id="' + ytbutton_elements_location_dict[
                                                                        "yt_id_sub_button_type1"] + '"]')
                            subscribe_button.click()
                            time.sleep(5)

                            log_message = f"<span style='color:blue'>[{gmail_account}]</span> <span style='color:green'> Subscribed on Youtube.com/{video_id}!</span>"
                            log_function(log_message)



                            break
                        except NoSuchElementException:
                            bypass_other_popup(browser)  # Handle popups

                    print("Subscribed")
                else:
                    print("Already subscribed")
                    log_message = f"<span style='color:blue'>[{gmail_account}]</span> <span style='color:red'> Already Subscribed on Youtube.com/{video_id}!</span>"
                    log_function(log_message)

            else:
                print("skip sub")

            if whatdata.get("like"):


                dump_status_update(row_data, active_instances_data, "Liking", excel_table, current_row, browser)


                liked = False  # Initialize variable to track like status
                try:
                    liked_element = browser.find_element(By.CSS_SELECTOR,
                                                         ytbutton_elements_location_dict["yt_css_like_button_active"])
                    liked = True
                except NoSuchElementException:
                    pass

                if not liked:  # Only like if not already liked
                    while True:
                        try:
                            print("clicking like")



                            like_button = browser.find_element(By.XPATH, '//*[@id="' + ytbutton_elements_location_dict[
                                "yt_id_like_button"] + '"]')
                            like_button.click()
                            time.sleep(5)

                            log_message = f"<span style='color:blue'>[{gmail_account}]</span> <span style='color:green'> Liked on Youtube.com/{video_id}!</span>"
                            log_function(log_message)



                            break
                        except NoSuchElementException:
                            bypass_other_popup(browser)  # Handle popups

                    print("Liked")
                else:
                    print("Already liked")
                    log_message = f"<span style='color:blue'>[{gmail_account}]</span> <span style='color:red'> Already Liked on Youtube.com/{video_id}!</span>"
                    log_function(log_message)

            else:
                print("skip like")

            if whatdata.get("comment"):
                while True:
                    try:

                        dump_status_update(row_data, active_instances_data, "Commenting", excel_table, current_row, browser)


                        print("Clicking comment")

                        # Scroll to the bottom of the page
                        browser.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
                        time.sleep(2)  # Wait for scrolling animation to complete

                        comment_placeholder = wait.until(
                            EC.visibility_of_element_located((By.XPATH, "//*[@id='simplebox-placeholder']")))


                        if comment_placeholder.is_displayed():
                            comment_placeholder.click()
                            time.sleep(2)  # Wait for scrolling animation to complete
                            try:
                                time.sleep(2)  # Wait for scrolling animation to complete

                                wait.until(EC.visibility_of_element_located(
                                    (By.XPATH, "//*[@id='contenteditable-root']"))).send_keys(
                                    whatdata.get("setcomment", ""))
                                time.sleep(5)

                                submit_button = wait.until(EC.visibility_of_element_located((By.XPATH,'/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-comments/ytd-item-section-renderer/div[1]/ytd-comments-header-renderer/div[5]/ytd-comment-simplebox-renderer/div[3]/ytd-comment-dialog-renderer/ytd-commentbox/div[2]/div/div[4]/div[5]/ytd-button-renderer[2]/yt-button-shape/button/yt-touch-feedback-shape/div')))
                                submit_button.click()

                                print("Commented: " + whatdata.get("setcomment", ""))

                                comment = whatdata.get("setcomment", "")

                                log_message = f"<span style='color:blue'>[{gmail_account}]</span> <span style='color:green'> Commented: <span style='color:yellow'> {comment}!</span> </span>"
                                log_function(log_message)

                                log_message = f"<span style='color:blue'>[{gmail_account}]</span> <span style='color:green'> Commented on Youtube.com/{video_id}!</span>"
                                log_function(log_message)

                                time.sleep(5)


                                break


                            except NoSuchElementException:
                                bypass_other_popup(browser)  # Handle popups



                    except NoSuchElementException:
                        bypass_other_popup(browser)  # Handle popups

            else:
                print("skip comment")



            time.sleep(2)  # Adjust the sleep time if necessary

            log_message = f"<span style='color:blue'>[{gmail_account}]</span> <span style='color:green'> All Actions are Complete!</span>"
            log_function(log_message)


            dump_status_update(row_data, active_instances_data, "All Actions Completed", excel_table, current_row, browser)


            browser.quit()

    except Exception as e:
        error_message = f"<span style='color:blue'>[{gmail_account}]</span> <span style='color:red'> Error occurred: {str(e)}</span>"
        log_function(error_message)

        traceback.print_exc()  # Print the traceback for debugging purposes
        log_function(traceback)
        # Handle the error as needed, such as logging, updating status, etc.




    finally:
        try:
            browser.quit()
        except Exception:
            pass



