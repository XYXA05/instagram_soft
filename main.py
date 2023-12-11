from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time 
import random
from log import username, password
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException



def logon(username, password):
    browser = webdriver.Chrome()
    try:
        browser.get('https://www.instagram.com/')
        time.sleep(random.randrange(3,6))

        username_input = browser.find_element(By.NAME,'username')
        username_input.clear()
        username_input.send_keys(username)

        time.sleep(3)

        password_input = browser.find_element(By.NAME,'password')
        password_input.clear()
        password_input.send_keys(password)

        password_input.send_keys(Keys.ENTER)

        time.sleep(10)

        browser.get('https://www.instagram.com/bogsai042023/followers/')
        time.sleep(10)

        followers_list = browser.find_element(By.XPATH, "//html/body/div[5]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]")
        for _ in range(10):  # You can adjust the number of times you want to scroll
            browser.execute_script("arguments[0].scrollBy(0, 1000);", followers_list)
            time.sleep(2)

        hrefs = list(set(map(lambda x: x.text, browser.find_elements(By.CLASS_NAME,'xt0psk2'))))
        hrefs = ['bogsai042023','_mertviy_anarxist_']
        print(hrefs)
        time.sleep(10)

        for href in hrefs:
            browser.get(f'https://www.instagram.com/{href}/')
            time.sleep(20)
            try:
                button_massage = browser.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/div[1]/div[1]/div/div[2]/div').click()
                time.sleep(10)
                browser.execute_script("document.getElementsByClassName('_a9-- _a9_1')[0].click()")
                time.sleep(20)
                button_massage = browser.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div[2]/div/div/div[2]/div/div/div[2]/div/div[1]')
                button_massage.clear()
                button_massage.send_keys('text')
                time.sleep(3)
                button_massage.send_keys(Keys.ENTER)

        #time.sleep(10)
            except NoSuchElementException:
                print(f"Element not found for profile: {href}")

    except Exception as q:
        print(q)


