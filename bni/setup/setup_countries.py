import json

from bni.db.db import session
from bni.model.data_model import Country


def update_db_with_countries():
    with open("config/countries.json", "r") as f:
        countries_data = json.load(f)

    for country_code, details in countries_data.items():
        existing = session.query(Country).filter_by(country_code=country_code).first()
        if existing:
            # Update existing record
            existing.country_name = details["country_name"]
            existing.country_url = details["country_url"]
        else:
            # Insert new record
            new_country = Country(
                country_code=country_code,
                country_name=details["country_name"],
                country_url=details["country_url"],
                country_id=details["country_id"]
            )
            session.add(new_country)

    session.commit()
