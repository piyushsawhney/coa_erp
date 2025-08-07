import time

from selenium.webdriver.common.by import By

from bni.chapter_data import driver

data = []
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

def get_mobile_from_profile():
    element = driver.find_element(By.CSS_SELECTOR, "a.moredots")
    driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", element)
    time.sleep(2)
    element.click()
    time.sleep(2)
    contact_divs = driver.find_elements(By.CSS_SELECTOR, "div.memberContactDetails[style*='display: block']")
    for div in contact_divs:
        # Find all <li> elements under this visible div
        li_elements = div.find_elements(By.TAG_NAME, "li")

        for li in li_elements:
            try:
                label = li.find_element(By.TAG_NAME, "strong").text.strip()
                if label.lower() == "phone":
                    phone = li.find_element(By.TAG_NAME, "a").text.strip()
                    return phone
            except:
                continue
    return None

def get_email_mobile_from_profile():
    email_link = get_email_link_from_profile()
    mobile = get_mobile_from_profile()
    return mobile,email_link


def navigate_members_in_a_chapter(chapter_link):
    driver.get(chapter_link)
    time.sleep(2)
    MEMBERS_TAB = "members_tab"
    member_tab_element = driver.find_element(By.ID, MEMBERS_TAB)
    driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", member_tab_element)
    time.sleep(1)
    member_tab_element.click()
    time.sleep(2)

    rows = driver.find_elements(By.CSS_SELECTOR, "#chapterListTable tbody tr")
    for row in rows:
        time.sleep(3)
        tds = row.find_elements(By.TAG_NAME, "td")
        if len(tds) >= 3:
            profile_link_tag = tds[0].find_element(By.TAG_NAME, "a")
            profile_url = profile_link_tag.get_attribute("href")
            member_name = profile_link_tag.text.strip()
            company_name = tds[1].text.strip()
            profession = tds[2].text.strip()
            profile_link_tag.click()
            time.sleep(2)
            mobile, email = get_email_mobile_from_profile()
            data.append({
                "Name": member_name,
                "Profile Link": profile_url,
                "Company": company_name,
                "Profession": profession,
                "Mobile": mobile,
                "Email": email
            })
            print(data)
            driver.get(chapter_link)
            time.sleep(5)
            driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });",
                                  member_tab_element)

navigate_members_in_a_chapter("https://bni.ae/en-AE/chapterdetail?chapterId=bnqo86407Crr7QvFAkiJxg%3D%3D&name=BNI+BNI+Gazelles")
