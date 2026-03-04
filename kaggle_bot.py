from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import random

def add_emails_to_kaggle(emails):

    chrome_options = webdriver.ChromeOptions()

    # Use your real Chrome profile
    chrome_options.add_argument(
        "user-data-dir=/Users/vaishnaviyeddula/Library/Application Support/Google/Chrome"
    )
    chrome_options.add_argument("profile-directory=Default")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

    # Go directly to permitted list page
    driver.get("YOUR_PERMITTED_LIST_URL")

    time.sleep(5)

    batch_size = 50

    for i in range(0, len(emails), batch_size):
        batch = emails[i:i+batch_size]

        textarea = driver.find_element(By.TAG_NAME, "textarea")
        textarea.clear()
        textarea.send_keys("\n".join(batch))

        save_button = driver.find_element(By.XPATH, "//button[contains(text(),'Save')]")
        save_button.click()

        time.sleep(random.randint(6,10))

    driver.quit()
