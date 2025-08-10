from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait

from bni.db.db import session
from bni.model.data_model import Country, Region
from bni.setup.selenium_setup import driver


def retrieve_region_options():
    return WebDriverWait(
        driver,
        timeout=15,
        poll_frequency=1,
        ignored_exceptions=[NoSuchElementException]
    ).until(EC.presence_of_element_located((By.ID, "regionId")))


def get_country_regions(country_url, country_code):
    country_search_url = country_url + "advancedchaptersearch"
    driver.get(country_search_url)
    select_element = retrieve_region_options()
    dropdown = Select(select_element)
    region_codes = set()
    for option in dropdown.options[1:]:
        region_code = option.get_attribute("value")
        region_name = option.text.strip()
        if not region_code:  # skip invalid
            continue
        region_codes.add(region_code)
        existing = session.query(Region).filter_by(region_code=region_code).first()
        if existing:
            existing.region_name = region_name
            existing.country_code = country_code
        else:
            new_region = Region(
                region_code=region_code,
                country_code=country_code,
                region_name=region_name
            )
            session.add(new_region)
    session.commit()
    return region_codes
#
#
# def process_dropdown_navigation():
#     return WebDriverWait(
#         driver,
#         timeout=15,
#         poll_frequency=1,
#         ignored_exceptions=[NoSuchElementException]
#     ).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "#regionId option")))
#
#
# def iterate_over_regions():
#     driver.get(BNI_UAE_CHAPTER_SEARCH)
#     dropdown_options = process_dropdown_navigation()
#     length = len(dropdown_options)
#     start_region = start_parameters["start_region"]
#     for i in range(start_region, length):
#         if i != start_region:
#             dropdown_options = process_dropdown_navigation()
#         option = dropdown_options[i]
#         option.click()
#         find_button = WebDriverWait(
#             driver,
#             timeout=15,
#             poll_frequency=1,
#             ignored_exceptions=[NoSuchElementException]
#         ).until(EC.visibility_of_element_located((By.ID, "submit")))
#         driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", find_button)
#         driver.execute_script("window.scrollBy(0, 200);")
#         find_button.click()
#         chapter_length = 1
#         while chapter_length != 0:
#             chapter_length = process_chapter_navigation()
#             driver.get(BNI_UAE_CHAPTER_SEARCH)
#         start_parameters["start_region"] = i
#         update_json(start_parameters)
#     start_parameters["start_region"] = 1
#     update_json(start_parameters)
