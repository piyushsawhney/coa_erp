from datetime import timedelta, date

from sqlalchemy import or_

from bni.data_retrieval.chapters import get_region_chapters_new
from bni.data_retrieval.members import get_chapter_members, get_member_contact
from bni.data_retrieval.regions import get_country_regions
from bni.db.db import session
from bni.model.data_model import Country, Member, Chapter, Region
from bni.setup.setup_countries import update_db_with_countries

if __name__ == '__main__':
    update_db_with_countries()
    country_code = input("Enter country code: ").strip().upper()
    option = input(
        "Enter 1/2:\n1. Retrieve Member list for a country\n2. Load member contacts in database\n").strip().upper()
    country = session.query(Country).filter_by(country_code=country_code).first()
    if option == '1':
        region_codes = get_country_regions(country.country_url, country.country_code)
        for region_code in region_codes:
            chapter_links = get_region_chapters_new(country.country_url, country.country_id, region_code)
            if chapter_links:
                for index, chapter_link in enumerate(chapter_links):
                    print(f"Index: {index}, Country : {country_code}, Region: {region_code}, Chapter : {chapter_link}")
                    get_chapter_members(chapter_link)
    elif option == '2':
        six_months_ago = date.today() - timedelta(days=6 * 30)  # approx. 6 months
        members_in_country = (
            session.query(Member)
            .join(Member.chapter)
            .join(Chapter.region)
            .join(Region.country)
            .filter(Country.country_code == country_code)
            .filter(
                or_(
                    Member.updated_date < six_months_ago,
                    Member.updated_date.is_(None)
                )
            )
            .all()
        )
        for member in members_in_country:
            get_member_contact(country.country_url, member.member_profile_link)
    else:
        print("Invalid option. Exiting...")
