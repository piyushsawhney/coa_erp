import time
from datetime import date

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from bni.db.db import session
from bni.model.data_model import Member
from bni.navigation import navigate_to_members_tab_and_click, navigate_pagination
from bni.setup.selenium_setup import driver


def get_chapter_member_ids(chapter_link):
    has_pagination = True
    driver.get(chapter_link)
    navigate_to_members_tab_and_click()
    member_links_set = set()
    while has_pagination:
        anchors = driver.find_elements(By.CSS_SELECTOR,
                                       "#chapterListTable tbody tr[role='row'] a[href*='memberdetails']")
        member_links_set.update(a.get_attribute("href") for a in anchors[0:50] if a.get_attribute("href"))
        has_pagination = navigate_pagination()
    for index, member_link in enumerate(member_links_set):
        print(f"Index {index}: Member Link: {member_link}, Chapter Link: {chapter_link}")
        existing = session.query(Member).filter_by(member_id=member_link).first()
        if existing:
            existing.member_profile_link = member_link
            existing.chapter_code = chapter_link
        else:
            new_member = Member(
                member_id=member_link,
                chapter_code=chapter_link,
                member_profile_link=member_link)
            session.add(new_member)
    session.commit()


def get_mobile_from_profile():
    element = driver.find_element(By.CSS_SELECTOR, "a.moredots")
    driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", element)
    element.click()
    time.sleep(1)
    phone_number = None
    direct_number = None

    try:
        phone_element = driver.find_element(By.XPATH, "//li[strong[text()='Phone']]/a")
        phone_number = phone_element.text.strip()
    except NoSuchElementException:
        pass

    try:
        direct_element = driver.find_element(By.XPATH, "//li[strong[text()='Direct']]/a")
        direct_number = direct_element.text.strip()
    except NoSuchElementException:
        pass
    return phone_number, direct_number


def get_email_link_from_profile():
    email_link = None
    ul_blocks = driver.find_elements(By.CSS_SELECTOR, "ul.memberContactInfo")
    for ul in ul_blocks:
        a_tags = ul.find_elements(By.TAG_NAME, "a")
        for a in a_tags:
            href = a.get_attribute("href")
            if href and "sendmessage" in href:
                return href
    return email_link


def check_redirection(country_url):
    """Wait until Chrome redirects to target_url, then return True/False."""
    try:
        WebDriverWait(
            driver,
            timeout=2,
            poll_frequency=0.5,
        ).until(EC.url_to_be(f"{country_url}index"))
        return True
    except:
        return False


def get_email_mobile_from_profile():
    WebDriverWait(
        driver,
        timeout=15,
        poll_frequency=1,
        ignored_exceptions=[NoSuchElementException]
    ).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.moredots")))
    email_link = get_email_link_from_profile()
    phone1, phone2 = get_mobile_from_profile()
    return phone1, phone2, email_link


def get_member_details(country_url, member_link):
    print(f"Getting Member Details for {member_link}")
    driver.get(member_link)
    if check_redirection(country_url):
        return
    profile = WebDriverWait(
        driver,
        timeout=15,
        poll_frequency=1,
        ignored_exceptions=[NoSuchElementException]
    ).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.memberProfileInfo")))
    member_name = WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div.memberProfileInfo h2"))
    ).text.strip()
    member_company = profile.find_element(By.CSS_SELECTOR, "div.memberProfileInfo p").text.strip()
    member_profession = profile.find_element(By.CSS_SELECTOR, "div.memberProfileInfo h6").text.strip()
    phone1, phone2, email_link = get_email_mobile_from_profile()
    today = date.today()
    print(member_name)
    session.query(Member).filter_by(member_id=member_link).update({
        Member.name: member_name,
        Member.company: member_company,
        Member.designation: member_profession,
        Member.phone: phone2,
        Member.mobile: phone1,
        Member.email_urls: email_link,
        Member.updated_date: today
    })
    session.commit()
