from sqlalchemy import Column, String, ForeignKey, Text, Date, func
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
    regions = relationship(
        "Region",
        back_populates="country",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

# 2. Region Table
class Region(Base):
    __tablename__ = "regions"

    region_code = Column(String(20), primary_key=True)
    country_code = Column(
        String(10),
        ForeignKey("countries.country_code", ondelete="CASCADE"),
        nullable=False
    )
    region_name = Column(String(255), nullable=False)

    # Relationships
    country = relationship("Country", back_populates="regions")
    chapters = relationship(
        "Chapter",
        back_populates="region",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

# 3. Chapter Table
class Chapter(Base):
    __tablename__ = "chapters"

    chapter_code = Column(String(255), primary_key=True)
    region_code = Column(
        String(20),
        ForeignKey("regions.region_code", ondelete="CASCADE"),
        nullable=False
    )
    chapter_name = Column(String(255), nullable=False)
    chapter_link = Column(String(255), nullable=False)

    # Relationships
    region = relationship("Region", back_populates="chapters")
    members = relationship(
        "Member",
        back_populates="chapter",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

# 4. Member Table
class Member(Base):
    __tablename__ = "members"

    member_id = Column(String(255), primary_key=True)
    chapter_code = Column(
        String(255),
        ForeignKey("chapters.chapter_code", ondelete="CASCADE"),
        nullable=False
    )
    member_profile_link = Column(String(255), nullable=False)
    name = Column(String(255), nullable=True)
    company = Column(String(255))
    designation = Column(Text)
    email_urls = Column(String(255))
    mobile = Column(String(50))
    phone = Column(String(50))
    updated_date = Column(Date)

    # Relationships
    chapter = relationship("Chapter", back_populates="members")
