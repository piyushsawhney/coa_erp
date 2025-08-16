import time

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from bni.db.db import session
from bni.model.data_model import Chapter
from bni.setup.selenium_setup import driver


def get_region_chapters_new(country_url, country_id, region_code):
    navigation_url = f"{country_url}chapterlist?countryIds={country_id}&regionId={region_code}&chapterName=&chapterCity=&chapterArea=&chapterMeetingDay=&chapterMeetingTime=&chapterMeetingType="

    driver.get(navigation_url)
    time.sleep(1)
    tbody_element = WebDriverWait(
        driver,
        timeout=15,
        poll_frequency=1,
        ignored_exceptions=[NoSuchElementException]
    ).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#chapterListTable tbody")))

    if "No matches found" in tbody_element.text or "Please refine your search" in tbody_element.text:
        return
    WebDriverWait(
        driver,
        timeout=15,
        poll_frequency=1,
        ignored_exceptions=[NoSuchElementException]
    ).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "tbody tr[role='row']")))
    anchors = tbody_element.find_elements(By.CSS_SELECTOR, "a[href*='chapterdetail']")
    chapter_links = set()
    for index, a in enumerate(anchors):
        chapter_link = a.get_attribute("href")
        if chapter_link:
            chapter_name = a.text.strip()
            chapter_links.add(chapter_link)
            chapter_code = chapter_link
            print(f"Index: {index}, Chapter Name : {chapter_name}, Region Code: {region_code}")
            if not chapter_code or not chapter_link:
                continue  # skip if no chapter code found
            chapter_links.add(chapter_link)

            # Insert or update in DB
            existing = session.query(Chapter).filter_by(chapter_code=chapter_code).first()
            if existing:
                existing.chapter_name = chapter_name
                existing.chapter_link = chapter_link
                existing.region_code = region_code
            else:
                new_chapter = Chapter(
                    chapter_code=chapter_code,
                    region_code=region_code,
                    chapter_name=chapter_name,
                    chapter_link=chapter_link
                )
                session.add(new_chapter)
    session.commit()
    return chapter_links
