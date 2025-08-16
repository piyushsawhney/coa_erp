import random

from bni.data_retrieval.chapters import get_region_chapters_new
from bni.data_retrieval.members_new import get_chapter_member_ids
from bni.data_retrieval.regions import get_country_regions
from bni.db.db import session
from bni.model.data_model import Country
from bni.setup.setup_countries import update_db_with_countries

if __name__ == '__main__':
    update_db_with_countries()
    country_code = input("Enter country code: ").strip().upper()
    country = session.query(Country).filter_by(country_code=country_code).first()
    region_codes = get_country_regions(country.country_url, country.country_code)
    for index, region_code in enumerate(random.sample(list(region_codes), len(region_codes))):
        chapter_links = get_region_chapters_new(country.country_url, country.country_id, region_code)
        if chapter_links:
            for index, chapter_link in enumerate(random.sample(list(chapter_links), len(chapter_links))):
                print(f"Index: {index}, Country : {country_code}, Region: {region_code}, Chapter : {chapter_link}")
                get_chapter_member_ids(chapter_link)
