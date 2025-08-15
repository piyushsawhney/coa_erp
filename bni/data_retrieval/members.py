import time
from datetime import date
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from bni.db.db import session
from bni.model.data_model import Member
from bni.setup.selenium_setup import driver


def navigate_to_members_tab_and_click(to_click=True):
    member_tab_id = "members_tab"
    member_tab_element = WebDriverWait(
        driver,
        timeout=15,
        poll_frequency=1,
        ignored_exceptions=[NoSuchElementException]
    ).until(EC.visibility_of_element_located((By.ID, member_tab_id)))
    driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", member_tab_element)
    driver.execute_script("window.scrollBy(0, 800);")
    member_tab_button = WebDriverWait(
        driver,
        timeout=15,
        poll_frequency=1,
        ignored_exceptions=[NoSuchElementException]
    ).until(EC.element_to_be_clickable((By.ID, member_tab_id)))
    if to_click:
        member_tab_button.click()


def navigate_pagination():
    next_button = WebDriverWait(
        driver,
        timeout=15,
        poll_frequency=1,
        ignored_exceptions=[NoSuchElementException]
    ).until(EC.presence_of_element_located((By.ID, "chapterListTable_next")))
    if "disabled" not in next_button.get_attribute("class"):
        next_a = next_button.find_element(By.TAG_NAME, "a")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_a)
        time.sleep(2)
        driver.execute_script("window.scrollBy(0, 600);")
        next_a.click()
        driver.execute_script("window.scrollTo({top: 200, behavior: 'smooth'});")


def render_table():
    wait = WebDriverWait(driver, 15, poll_frequency=1, ignored_exceptions=[NoSuchElementException])

    # Wait until either real rows OR no-results row appears
    wait.until(
        lambda d: d.find_elements(By.CSS_SELECTOR, "#chapterListTable tbody tr[role='row']") or
                  d.find_elements(By.CSS_SELECTOR, "#chapterListTable tbody tr td.dataTables_empty")
    )
    return driver.find_elements(By.CSS_SELECTOR, "#chapterListTable tbody tr[role='row']")


def get_members_details(chapter_link):
    rows = render_table()
    if not rows:
        return None
    for index, row in enumerate(rows):
        if index != 0 and index % 50 == 0:
            navigate_pagination()
            time.sleep(2)
            render_table()
        cols = row.find_elements(By.TAG_NAME, "td")
        if len(cols) < 1:
            continue  # skip malformed rows
        name_elem = cols[0].find_element(By.TAG_NAME, "a")
        member_name = name_elem.text.strip()
        print(f"Index: {index}, Member Name: {member_name}, Chapter Link: {chapter_link}")
        profile_link = name_elem.get_attribute("href")
        company_name = cols[1].text.strip()
        profession = cols[2].text.strip()
        member_id = profile_link

        # Insert or update in DB
        existing = session.query(Member).filter_by(member_id=member_id).first()
        if existing:
            existing.name = member_name
            existing.member_profile_link = profile_link
            existing.chapter_code = chapter_link
        else:
            new_member = Member(
                member_id=member_id,
                chapter_code=chapter_link,
                member_profile_link=profile_link,
                name=member_name,
                company=company_name,
                designation=profession)
            session.add(new_member)
    session.commit()


def get_chapter_members(chapter_link):
    driver.get(chapter_link)
    navigate_to_members_tab_and_click()
    get_members_details(chapter_link)


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
            timeout=3,
            poll_frequency=0.5,
        ).until(EC.url_to_be(f"{country_url}index"))
        return True
    except:
        return False


def get_member_contact(country_url,profile_link):
    print(profile_link)
    driver.get(profile_link)
    if check_redirection(country_url):
        return
    phone1, phone2, email_link = get_email_mobile_from_profile()
    today = date.today()
    session.query(Member).filter_by(member_id=profile_link).update({
        Member.phone: phone2,
        Member.mobile: phone1,
        Member.email_urls: email_link,
        Member.updated_date: today
    })
    session.commit()
