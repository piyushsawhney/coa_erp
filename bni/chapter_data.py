from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from bni.urls import BNI_UAE_CHAPTER_SEARCH

CHAPTER_DROPDOWN_ID = "select#regionId"
CHAPTER_PAGE_FIND_CSS = "button.button"


def navigate_chapter_members():
    pass


def get_chapter_links_in_region():
    a_tags = driver.find_elements(By.CSS_SELECTOR, "#chapterListTable tbody td a[href]")
    hrefs = [a.get_attribute("href") for a in a_tags]





driver = webdriver.Chrome()


def navigate_search():
    driver.get(BNI_UAE_CHAPTER_SEARCH)
    WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, CHAPTER_DROPDOWN_ID))
    )
    regions = driver.find_elements(By.CSS_SELECTOR, CHAPTER_DROPDOWN_ID)
    for region in regions:
        print(region.text)
