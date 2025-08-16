from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from bni.setup.selenium_setup import driver


def navigate_to_members_tab_and_click(to_scroll=True):
    members_tab = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "members_tab"))
    )
    driver.execute_script("arguments[0].click();", members_tab)


def navigate_pagination():
    li_next = WebDriverWait(
        driver,
        timeout=15,
        poll_frequency=1,
        ignored_exceptions=[NoSuchElementException]
    ).until(EC.presence_of_element_located((By.ID, "chapterListTable_next")))
    # check if disabled
    if "disabled" not in li_next.get_attribute("class"):
        next_button = li_next.find_element(By.TAG_NAME, "a")
        driver.execute_script("arguments[0].click();", next_button)
        return True
    return False
