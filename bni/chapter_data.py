from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
from bni.member_data import process_member_navigation
from bni.selenium_setup import driver


def get_chapter_list():
    return WebDriverWait(
        driver,
        timeout=15,
        poll_frequency=1,
        ignored_exceptions=[NoSuchElementException]
    ).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "#chapterListTable tbody tr")))


def process_chapter_navigation():
    total_rows = get_chapter_list()
    number_of_chapters = len(total_rows) ## It will always have one <tr> tag
    remaining_chapters = number_of_chapters
    if number_of_chapters > 1:
        for i in range(number_of_chapters):
            row = get_chapter_list()[i]
            tds = row.find_elements(By.TAG_NAME, "td")
            if len(tds) >= 3:
                chapter_link = WebDriverWait(tds[0], 10).until(
                    EC.element_to_be_clickable((By.TAG_NAME, "a"))
                )
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                                      chapter_link)
                time.sleep(1)
                driver.execute_script("window.scrollBy(0, 600);")
                chapter_link.click()
                no_of_members = 1
                while no_of_members != 0:
                    no_of_members = process_member_navigation()
                    driver.back()
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                remaining_chapters -= remaining_chapters
                if remaining_chapters == 0:
                    return 0
    return 0
