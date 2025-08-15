from bni.data_retrieval.members import get_member_contact
from bni.db.db import session
from bni.model.data_model import Member, Chapter, Region

if __name__ == '__main__':
    members_in_country = (
        session.query(Member)
        .join(Member.chapter)
        .join(Chapter.region)
        .join(Region.country)
        .filter(Member.updated_date.is_(None))
        .all()
    )
    for member in members_in_country:
        country = member.chapter.region.country
        get_member_contact(country.country_url, member.member_profile_link)
