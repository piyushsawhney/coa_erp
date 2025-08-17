import os

from openpyxl import Workbook
from sqlalchemy.orm import Session

from bni.db.db import session
from bni.model.data_model import Country, Member, Region, Chapter


def export_members_to_excel_per_country(output_dir):
    """
    Create one Excel file per country with all members.

    Args:
        session (Session): SQLAlchemy session
        output_dir (str): Folder where Excel files will be saved
    """
    os.makedirs(output_dir, exist_ok=True)

    # Query all countries
    countries = session.query(Country).all()

    for country in countries:
        # Create workbook
        wb = Workbook()
        ws = wb.active
        ws.title = "Members"

        # Add headers
        ws.append([
            "Country Name",
            "Chapter Name",
            "Member Name",
            "Mobile",
            "Email",
            "Phone",
            "Company",
            "Profession",
            "Member Link"
        ])

        # Query members by joining tables
        members = (
            session.query(Member)
            .join(Member.chapter)
            .join(Chapter.region)
            .join(Region.country)
            .filter(Country.country_code == country.country_code)
            .all()
        )

        # Write rows
        for member in members:
            ws.append([
                country.country_name,
                member.chapter.chapter_name if member.chapter else "",
                member.name or "",
                member.mobile or "",
                member.email_urls or "",
                member.phone or "",
                member.company or "",
                member.designation or "",
                member.member_profile_link or ""
            ])

        # Save file
        file_path = os.path.join(output_dir, f"{country.country_code}.xlsx")
        wb.save(file_path)
        print(f"✅ Saved {os.path.abspath(output_dir)}, File Name{file_path}")


export_members_to_excel_per_country(output_dir="country_excels")
