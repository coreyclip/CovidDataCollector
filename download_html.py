
import time
import os
import json
import pandas as pd
from datetime import datetime as dt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def wait_for(selector,method, seconds):
    wait = WebDriverWait(driver, seconds)
    try:
        if method == "css":
            wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, selector)))
        elif method == "name":
            wait.until(expected_conditions.visibility_of_element_located((By.NAME, selector)))
        else:
            raise Exception(f'unrecognized method: {method}')
    except Exception as e:
        print(f"timeout on: {selector}")
        raise e


timestamp = dt.now().strftime("%m-%d-%Y")
if not os.path.isdir(timestamp):
    os.mkdir(timestamp)
driver = webdriver.Firefox()
driver.get("http://dashboard.publichealth.lacounty.gov/covid19_surveillance_dashboard/")
try:
    driver.set_window_size(1099, 694)
    driver.switch_to.frame(0)
    wait_for("li:nth-child(5) span", "css", 10)
    # download first table
    driver.find_element(By.CSS_SELECTOR, "li:nth-child(5) span").click()
    try:
        wait_for("DataTables_Table_0_length", "name", 5)
    except:
        driver.find_element(By.CSS_SELECTOR, "li:nth-child(5) span").click()
        wait_for("DataTables_Table_0_length", "name", 10)
    driver.find_element(By.NAME, "DataTables_Table_0_length").click()
    dropdown = driver.find_element(By.NAME, "DataTables_Table_0_length")
    dropdown.find_element(By.XPATH, "//option[. = 'All']").click()
    time.sleep(2)
    wait_for("option:nth-child(3)", "css", 10)
    driver.find_element(By.CSS_SELECTOR, "option:nth-child(3)").click()
    time.sleep(5)
    table = driver.find_element(By.ID, "DataTables_Table_0").get_attribute("outerHTML")
    df = pd.read_html(table)[0]
    df["timestamp"] = dt.now()
    df.to_csv(os.path.join(timestamp, "LA_County_Covid19_CSA_case_death_table.csv"))
    driver.find_element(By.CSS_SELECTOR, "li:nth-child(6) span").click()
    try:
        wait_for("DataTables_Table_1_length", "name", 5)
    except:
        driver.find_element(By.CSS_SELECTOR, "li:nth-child(6) span").click()
        wait_for("DataTables_Table_1_length", "name", 10)
    driver.find_element(By.NAME, "DataTables_Table_1_length").click()
    dropdown = driver.find_element(By.NAME, "DataTables_Table_1_length")
    dropdown.find_element(By.XPATH, "//option[. = 'All']").click()
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, "#DataTables_Table_1_length option:nth-child(3)").click()
    time.sleep(5)
    table = driver.find_element(By.ID, "DataTables_Table_1").get_attribute("outerHTML")
    df = pd.read_html(table)[0]
    df["timestamp"] = dt.now()
    df.to_csv(os.path.join(timestamp, "LA_County_Covid19_CSA_testing_table.csv"))
    import pdb; pdb.set_trace()
    driver.quit()
except Exception as e:
    driver.quit()
    raise e
