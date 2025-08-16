from sqlalchemy import or_

from bni.data_retrieval.members_new import get_member_details
from bni.db.db import session
from bni.model.data_model import Member, Chapter, Region

if __name__ == '__main__':
    members_in_country = (
        session.query(Member)
        .join(Member.chapter)
        .join(Chapter.region)
        .join(Region.country)
        .filter(
            or_(Member.email_urls.is_(None), Member.email_urls == ""),
            or_(Member.mobile.is_(None), Member.mobile == ""),
            or_(Member.phone.is_(None), Member.phone == "")
        )
        .all()
    )
    for member in members_in_country:
        print(member.name)
        country = member.chapter.region.country
        get_member_details(country.country_url, member.member_profile_link)
