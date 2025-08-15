from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from bni.db.db import session
from bni.model.data_model import Chapter
from bni.setup.selenium_setup import driver


def get_region_chapters(country_url,country_id, region_code):
    print(f"{country_id}/{region_code}")
    navigation_url = f"{country_url}chapterlist?countryIds={country_id}&regionId={region_code}&chapterName=&chapterCity=&chapterArea=&chapterMeetingDay=&chapterMeetingTime=&chapterMeetingType="
    driver.get(navigation_url)
    # navigate_to_members_tab_and_click()
    wait = WebDriverWait(driver, 15, poll_frequency=1, ignored_exceptions=[NoSuchElementException])

    # Wait until either real rows OR no-results row appears
    wait.until(
        lambda d: d.find_elements(By.CSS_SELECTOR, "tbody tr[role='row']") or
                  d.find_elements(By.CSS_SELECTOR, "tbody tr td.dataTables_empty")
    )
    chapter_links = set()
    rows = driver.find_elements(By.CSS_SELECTOR, "tbody tr[role='row']")
    if not rows:
        return None
    for row in rows:
        first_td = row.find_element(By.TAG_NAME, "td")
        a_tag = first_td.find_element(By.TAG_NAME, "a")

        chapter_name = a_tag.text.strip()
        print(chapter_name)
        chapter_link = a_tag.get_attribute("href")
        chapter_code = chapter_link

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
