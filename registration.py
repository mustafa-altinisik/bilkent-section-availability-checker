from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import sys
import os
import requests

#Telegram configuration is optional
def send_telegram_message(message, bot_token, chat_id):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message
    }
    response = requests.post(url, data=data)
    return response.json()

bot_token = "YOUR_BOT_TOKEN"#Replace it with your bot token
chat_id = "CHAT_ID"#Make your bot admin in one of group chats and put its id here


def sound_alert(message="Alert"):
    while True:
        os.system(f'say {message}')

main_page_url = "https://stars.bilkent.edu.tr/homepage/plain_offerings"
#EDEB-110 is in the first row, so the td value is 1
edeb_xpath = "//*[@id='EDEB']/td[1]"
#The sections I am after are the first and the second.
quota_cell_xpaths = [
    "//*[@id='poTable']/tbody/tr[1]/td[14]",
    "//*[@id='poTable']/tbody/tr[2]/td[14]"
] 
refresh_interval = 5 
first_iteration_wait = 60

# Initialize the browser
browser = webdriver.Chrome()

first_iteration = True

try:
    while True:
        browser.get(main_page_url)

        if first_iteration:
            time.sleep(first_iteration_wait)
            first_iteration = False
        else:
            time.sleep(5)

        # Click on the EDEB course category
        edeb_course_row = browser.find_element(By.XPATH, edeb_xpath)
        edeb_course_row.click()
        time.sleep(5)

        # Check quotas for specified rows
        for quota_xpath in quota_cell_xpaths:
            quota_cell = browser.find_element(By.XPATH, quota_xpath)
            quota = int(quota_cell.text)

            if quota > 0:
                send_telegram_message("Spot Available For: ", bot_token, chat_id)
                print(f"Spot available, Quota: {quota}")
                sound_alert("Spot available")

            else:
                print("Section not available at: " + time.strftime("%H:%M:%S"))



        time.sleep(refresh_interval)

except Exception as e:
    print(f"An error occurred: {e}", file=sys.stderr)
finally:
    pass
