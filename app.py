from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

def check_website():
    driver = None
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install())

        # URL ওপেন করা
        url = "https://www.goethe.de/ins/bd/en/spr/prf/gzb1.cfm"
        driver.get(url)

        # Select Module চেক করা
        try:
            element = driver.find_element(By.XPATH, "//*[contains(text(), 'Select Module')]")
            print("Condition Met: 'Select Module' found!")
        except NoSuchElementException:
            print("Condition Not Met: 'Select Module' not found.")

    finally:
        if driver is not None:
            driver.quit()

check_website()
