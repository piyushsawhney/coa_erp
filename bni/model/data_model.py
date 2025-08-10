from sqlalchemy import Column, String, ForeignKey, Text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

# 1. Country Table
class Country(Base):
    __tablename__ = "countries"

    country_code = Column(String(10), primary_key=True)
    country_name = Column(String(100), nullable=False)
    country_url = Column(String(255), nullable=False)
    country_id = Column(String(10), nullable=False, unique=True)

    # Relationship to Regions
    regions = relationship("Region", back_populates="country")

# 2. Region Table
class Region(Base):
    __tablename__ = "regions"

    region_code = Column(String(20), primary_key=True)
    country_code = Column(String(10), ForeignKey("countries.country_code"), nullable=False)
    region_name = Column(String(100), nullable=False)

    # Relationships
    country = relationship("Country", back_populates="regions")
    chapters = relationship("Chapter", back_populates="region")

# 3. Chapter Table
class Chapter(Base):
    __tablename__ = "chapters"

    chapter_code = Column(String(20), primary_key=True)
    region_code = Column(String(20), ForeignKey("regions.region_code"), nullable=False)
    chapter_name = Column(String(100), nullable=False)
    chapter_link = Column(String(255), nullable=False)

    # Relationships
    region = relationship("Region", back_populates="chapters")
    members = relationship("Member", back_populates="chapter")

# 4. Member Table
class Member(Base):
    __tablename__ = "members"

    member_id = Column(String(50), primary_key=True)  # Could also use chapter_code+name
    chapter_code = Column(String(20), ForeignKey("chapters.chapter_code"), nullable=False)
    member_profile_link = Column(String(255), nullable=False)
    name = Column(String(100), nullable=False)
    company = Column(String(100))
    designation = Column(Text)
    email_urls = Column(String(255))
    mobile = Column(String(50))
    phone = Column(String(50))

    # Relationships
    chapter = relationship("Chapter", back_populates="members")
