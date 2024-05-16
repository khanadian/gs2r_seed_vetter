from selenium import webdriver
from tkinter import simpledialog
from datetime import datetime
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

def credential(driver, url):
    #driver.set_window_position(2000, 100)
    #driver.maximize_window()

    #logging in
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(\
    (By.XPATH, "//input[@type='text']")))
    textfields = driver.find_elements(By.XPATH,"//input[@type='text']")
    passfield = driver.find_element(By.XPATH,"//input[@type='password']")
    specbox = driver.find_element(By.XPATH,"//input[@type='checkbox']")
    join_button = driver.find_element(By.XPATH,"//input[@type='submit']")
    for field in textfields:
        if not field.get_attribute("readonly"):
            field.send_keys("script")
    passfield.send_keys("neo")
    specbox.click()
    join_button.click()

    # grabbing the objectives
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(\
    (By.CSS_SELECTOR, ".vertical-center.text-container")))
    objs = driver.find_elements(By.CSS_SELECTOR, ".vertical-center.text-container")
    objectives = [[]]
    index1 = 0
    counter = 0
    for obj in objs:
        if counter == 5:
            counter = 0
            objectives.append([])
            index1 += 1
        print(obj.text)
        objectives[index1].append(obj.text)
        counter += 1
    return objectives
    
    
        

start_time = time.time()
print(datetime.now())

url = "https://bingosync.karanum.xyz/room/_ehTIGtfQHK8zV6ybQqR5Q"#simpledialog.askstring("Bingo", "url")
#print(url)
driver = webdriver.Chrome(ChromeDriverManager().install())

obj = credential(driver, url)
print(obj)

time.sleep(5)

driver.close()
driver.quit()

