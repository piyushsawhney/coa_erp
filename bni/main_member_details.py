from sqlalchemy import or_

from bni.data_retrieval.members_new import get_member_details
from bni.db.db import session
from bni.model.data_model import Member, Chapter, Region


def get_members_from_db():
    return (
        session.query(Member)
        .join(Member.chapter)
        .join(Chapter.region)
        .join(Region.country)
        .filter(
            or_(Member.email_urls.is_(None), Member.email_urls == ""),
            or_(Member.mobile.is_(None), Member.mobile == ""),
            or_(Member.phone.is_(None), Member.phone == "")
        )
        .limit(10)
        .all()
    )


if __name__ == '__main__':
    members_left = 1
    while members_left:
        members_in_country = get_members_from_db()
        for member in members_in_country:
            country = member.chapter.region.country
            get_member_details(country.country_url, member.member_profile_link, member)
        members_left = len(members_in_country)
