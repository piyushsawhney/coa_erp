from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from bni.chapter_data import process_chapter_navigation
from bni.selenium_setup import driver
from bni.urls import BNI_UAE_CHAPTER_SEARCH

data = []


def process_dropdown_navigation():
    return WebDriverWait(
        driver,
        timeout=15,
        poll_frequency=1,
        ignored_exceptions=[NoSuchElementException]
    ).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "#regionId option")))


def iterate_over_regions():
    driver.get(BNI_UAE_CHAPTER_SEARCH)
    dropdown_options = process_dropdown_navigation()
    length = len(dropdown_options)
    for i in range(1, length + 1):
        if i != 1:
            dropdown_options = process_dropdown_navigation()
        option = dropdown_options[i]
        option.click()
        find_button = WebDriverWait(
            driver,
            timeout=15,
            poll_frequency=1,
            ignored_exceptions=[NoSuchElementException]
        ).until(EC.visibility_of_element_located((By.ID, "submit")))
        driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", find_button)
        driver.execute_script("window.scrollBy(0, 200);")
        find_button.click()
        chapter_length = 1
        while chapter_length != 0:
            chapter_length = process_chapter_navigation()
            driver.get(BNI_UAE_CHAPTER_SEARCH)


iterate_over_regions()
