import os
import uuid

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs, AsyncEngine, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import Final, Optional, List
from sqlalchemy import (
    DateTime, String,
    func, Text, ForeignKey,
    Boolean, Integer, BigInteger,
    Enum, Date, JSON, Numeric, UniqueConstraint
)
from datetime import datetime, date
from sqlalchemy.pool import NullPool
from sqlalchemy.dialects.postgresql import UUID
from configs.db.enums import (
    MediaType, ProficiencyEnum, EmploymentTypeEnum,
    EmploymentStatusEnum, ExperienceLevelEnum,
    EducationLevelEnum, VacancyStatusEnum, WorkplaceTypeEnum,
    AddressTypeEnum, ApplicationStatusEnum, ApplicationSourceEnum, ReactionTypeEnum
)

load_dotenv()

DATABASE_URL: Final[str | None] = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise ValueError("DATABASE_URL is None")

engine: Final[AsyncEngine] = create_async_engine(DATABASE_URL, future=True, poolclass=NullPool)

AsyncSessionLocal: Final[async_sessionmaker[AsyncSession]] = async_sessionmaker(engine, expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase):
    pass

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

class UserEntity(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(150), nullable=False, unique=True, index=True)
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)
    password: Mapped[str] = mapped_column(String(500), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_block: Mapped[bool] = mapped_column(Boolean, default=False)
    avatar_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    refresh_token: Mapped[str | None] = mapped_column(String(), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                 onupdate=func.now(), nullable=False)

    posts: Mapped[list["PostUserEntity"]] = relationship("PostUserEntity", back_populates="owner")
    categories: Mapped[list["CategoryEntity"]] = relationship("CategoryEntity", back_populates="owner")
    industries: Mapped[list["IndustryEntity"]] = relationship("IndustryEntity", back_populates="owner")

    enterprise: Mapped["EnterpriseEntity"] = relationship("EnterpriseEntity", back_populates="owner", uselist=False)
    curriculum: Mapped["CurriculumEntity"] = relationship("CurriculumEntity", back_populates="owner", uselist=False)

    favorite_post_user: Mapped[list["FavoritePostUserEntity"]] = relationship("FavoritePostUserEntity",
                                                                              back_populates="owner")
    my_skills: Mapped[list["MySkillEntity"]] = relationship("MySkillEntity", back_populates="owner")

    favorite_post_enterprise: Mapped[list["FavoritePostEnterpriseEntity"]] = relationship(
        "FavoritePostEnterpriseEntity", back_populates="owner")
    reviews: Mapped[list["ReviewEnterprise"]] = relationship("ReviewEnterprise", back_populates="owner")

    employments: Mapped[list["EmployeeEnterpriseEntity"]] = relationship("EmployeeEnterpriseEntity",
                                                                         back_populates="owner")
    searchs: Mapped[list["SavedSearchEntity"]] = relationship("SavedSearchEntity", back_populates="owner")

    areas: Mapped[list["AreaEntity"]] = relationship("AreaEntity", back_populates="owner")
    address: Mapped["AddressUserEntity"] = relationship("AddressUserEntity", back_populates="owner", uselist=False)

    applications: Mapped[List["ApplicationEntity"]] = relationship("ApplicationEntity", back_populates="user")

    comment_user_reactions: Mapped[List["ReactionCommentPostUserEntity"]] = relationship(
        "ReactionCommentPostUserEntity",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    following_relationships: Mapped[List["FollowerRelationshipEntity"]] = relationship(
        "FollowerRelationshipEntity",
        back_populates="follower",
        foreign_keys="[FollowerRelationshipEntity.follower_id]",
        cascade="all, delete-orphan",
    )

    followers_relationships: Mapped[List["FollowerRelationshipEntity"]] = relationship(
        "FollowerRelationshipEntity",
        back_populates="followed",
        foreign_keys="[FollowerRelationshipEntity.followed_id]",
        cascade="all, delete-orphan",
    )

    following_enterprises_relationships: Mapped[List["FollowerRelationshipEnterpriseEntity"]] = relationship(
        "FollowerRelationshipEnterpriseEntity",
        back_populates="follower",
        cascade="all, delete-orphan",
    )

    post_reactions: Mapped[List["ReactionPostUserEntity"]] = relationship(
        "ReactionPostUserEntity",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    enterprise_post_reactions: Mapped[List["ReactionPostEnterpriseEntity"]] = relationship(  # <--- NOVO
        "ReactionPostEnterpriseEntity",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    comments: Mapped[list["CommentPostUserEntity"]] = relationship(
        "CommentPostUserEntity",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    enterprise_post_comments: Mapped[List["CommentPostEnterpriseEntity"]] = relationship(
        "CommentPostEnterpriseEntity",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    favorite_comment_enterprise: Mapped[list["FavoriteCommentPostEnterpriseEntity"]] = relationship(
        "FavoriteCommentPostEnterpriseEntity",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    metric: Mapped["UserMetricEntity"] = relationship("UserMetricEntity", back_populates="owner", uselist=False)

    favorite_comment_user: Mapped[List["FavoriteCommentPostUserEntity"]] = relationship(
        "FavoriteCommentPostUserEntity",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    comment_enterprise_reactions: Mapped[list["ReactionCommentPostEnterpriseEntity"]] = relationship(
        "ReactionCommentPostEnterpriseEntity",
        back_populates="user",
        cascade="all, delete-orphan"
    )

class UserMetricEntity(Base):
    __tablename__ = "metric_users"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False, primary_key=True
    )

    post_count: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    favorite_post_count: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)

    comment_count: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    favorite_comment_count: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)

    follower_count: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    followed_count: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)

    share_count: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    connection_count: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)

    blocked_count: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)

    reaction_comment_given_count: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    reaction_comment_received_count: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)

    enterprise_follow_count: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    enterprise_follower_count: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)

    profile_view_count: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    vacancy_application_count: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)

    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                           nullable=True)
    last_post_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                          nullable=True)

    last_comment_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                             nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                 onupdate=func.now(), nullable=False)

    owner: Mapped["UserEntity"] = relationship("UserEntity", back_populates="metric", uselist=False)

class FollowerRelationshipEntity(Base):
    __tablename__ = "follower_relationships"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    follower_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    followed_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    follower: Mapped["UserEntity"] = relationship("UserEntity", foreign_keys=[follower_id],
                                                  back_populates="following_relationships")
    followed: Mapped["UserEntity"] = relationship("UserEntity", foreign_keys=[followed_id],
                                                  back_populates="followers_relationships")

class AddressUserEntity(Base):
    __tablename__ = "addresses_user"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False, index=True
    )

    street: Mapped[str] = mapped_column(String(255), nullable=False)
    number: Mapped[str] = mapped_column(String(50), nullable=True)
    complement: Mapped[str | None] = mapped_column(String(255), nullable=True)
    district: Mapped[str | None] = mapped_column(String(100), nullable=True)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    state: Mapped[str] = mapped_column(String(100), nullable=False)
    country: Mapped[str] = mapped_column(String(100), nullable=False, default="Brasil")
    zipcode: Mapped[str] = mapped_column(String(20), nullable=True)

    address_type: Mapped[AddressTypeEnum] = mapped_column(
        Enum(AddressTypeEnum, name="address_type_enum"),
        nullable=False,
        default=AddressTypeEnum.RESIDENTIAL
    )

    is_default: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                 onupdate=func.now(), nullable=False)

    owner: Mapped["UserEntity"] = relationship("UserEntity", back_populates="address")

class SavedSearchEntity(Base):
    __tablename__ = "saved_searches"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    query: Mapped[dict] = mapped_column(JSON, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_public: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    last_executed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    execution_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    notifications_enabled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

    owner: Mapped["UserEntity"] = relationship("UserEntity", back_populates="searchs")

class MySkillEntity(Base):
    __tablename__ = "my_skills"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False
    )

    skill_id: Mapped[int] = mapped_column(
        ForeignKey("skills.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False
    )

    proficiency: Mapped[ProficiencyEnum] = mapped_column(
        Enum(ProficiencyEnum, name="proficiency_enum"),
        default=ProficiencyEnum.basic,
        nullable=False
    )

    certificate_url: Mapped[str | None] = mapped_column(Text, nullable=True)

    datails: Mapped[str | None] = mapped_column(Text, nullable=True)

    years_of_experience: Mapped[int | None] = mapped_column(Integer, nullable=True)

    last_used_date: Mapped[date] = mapped_column(Date, server_default=func.now(), nullable=False)

    owner: Mapped["UserEntity"] = relationship("UserEntity", back_populates="my_skills")

    skill: Mapped["SkillEntity"] = relationship("SkillEntity", back_populates="my_skills")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                 onupdate=func.now(), nullable=False)

class SkillEntity(Base):
    __tablename__ = "skills"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                 onupdate=func.now(), nullable=False)

    my_skills: Mapped[list["MySkillEntity"]] = relationship("MySkillEntity", back_populates="skill")
    vacancies: Mapped[List["VacancySkillEntity"]] = relationship("VacancySkillEntity", back_populates="skill")

class CurriculumEntity(Base):
    __tablename__ = "curriculums"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), unique=True, nullable=False)

    title: Mapped[str] = mapped_column(String(150), nullable=False)
    is_updated: Mapped[bool] = mapped_column(Boolean, default=True)
    is_visible: Mapped[bool] = mapped_column(Boolean, default=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                 onupdate=func.now(), nullable=False)

    owner: Mapped["UserEntity"] = relationship("UserEntity", back_populates="curriculum")

class IndustryEntity(Base):
    __tablename__ = "industries"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    icon_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    usage_count: Mapped[int] = mapped_column(Integer, default=0)

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                 onupdate=func.now(), nullable=False)

    owner: Mapped["UserEntity"] = relationship("UserEntity", back_populates="industries")

    enterprises: Mapped[list["EnterpriseEntity"]] = relationship(
        "EnterpriseEntity", back_populates="industry"
    )

class AreaEntity(Base):
    __tablename__ = "areas"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                 onupdate=func.now(), nullable=False)

    owner: Mapped["UserEntity"] = relationship("UserEntity", back_populates="areas")

    vacancies: Mapped[list["VacancyEntity"]] = relationship(
        "VacancyEntity",
        back_populates="area"
    )

class EnterpriseEntity(Base):
    __tablename__ = "enterprises"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)

    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    website_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    logo_url: Mapped[str | None] = mapped_column(Text, nullable=True)

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), unique=True)

    industry_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("industries.id"))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                 onupdate=func.now(), nullable=False)

    owner: Mapped["UserEntity"] = relationship("UserEntity", back_populates="enterprise")
    address: Mapped["UserEntity"] = relationship("UserEntity", back_populates="enterprise")
    industry: Mapped["IndustryEntity"] = relationship("IndustryEntity", back_populates="enterprises")
    posts: Mapped[list["PostEnterpriseEntity"]] = relationship("PostEnterpriseEntity", back_populates="enterprise")
    reviews: Mapped[list["ReviewEnterprise"]] = relationship("ReviewEnterprise", back_populates="enterprise")
    employments: Mapped[list["EmployeeEnterpriseEntity"]] = relationship("EmployeeEnterpriseEntity",
                                                                         back_populates="enterprise")
    vacancies: Mapped[list["VacancyEntity"]] = relationship("VacancyEntity", back_populates="enterprise")

    address: Mapped["AddressEnterpriseEntity"] = relationship("AddressEnterpriseEntity", back_populates="enterprise")

    followers_relationships: Mapped[List["FollowerRelationshipEnterpriseEntity"]] = relationship(
        "FollowerRelationshipEnterpriseEntity",
        back_populates="followed_enterprise", cascade="all, delete-orphan",
    )

class FollowerRelationshipEnterpriseEntity(Base):
    __tablename__ = "follower_relationships_enterprise"

    __table_args__ = (
        UniqueConstraint("user_id", "enterprise_id", name="uq_user_enterprise_follow"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id")
    )

    enterprise_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("enterprises.id")
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    follower: Mapped["UserEntity"] = relationship(
        "UserEntity",
        foreign_keys=[user_id],
        back_populates="following_enterprises_relationships"
    )

    followed_enterprise: Mapped["EnterpriseEntity"] = relationship(
        "EnterpriseEntity",
        foreign_keys=[enterprise_id],
        back_populates="followers_relationships"
    )

class AddressEnterpriseEntity(Base):
    __tablename__ = "addresses_enterprise"

    enterprise_id: Mapped[int] = mapped_column(
        ForeignKey("enterprises.id"),
        nullable=False,
        index=True,
        primary_key=True,
    )

    street: Mapped[str] = mapped_column(String(255), nullable=False)
    number: Mapped[str] = mapped_column(String(50), nullable=True)
    complement: Mapped[str | None] = mapped_column(String(255), nullable=True)
    district: Mapped[str | None] = mapped_column(String(100), nullable=True)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    state: Mapped[str] = mapped_column(String(100), nullable=False)
    country: Mapped[str] = mapped_column(String(100), nullable=False)
    zipcode: Mapped[str] = mapped_column(String(20), nullable=True)

    address_type: Mapped[AddressTypeEnum] = mapped_column(
        Enum(AddressTypeEnum, name="address_type_enum"),
        nullable=False,
        default=AddressTypeEnum.RESIDENTIAL
    )

    is_default: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_public: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                 onupdate=func.now(), nullable=False)

    enterprise: Mapped["EnterpriseEntity"] = relationship("EnterpriseEntity", back_populates="address")

class VacancyEntity(Base):
    __tablename__ = "vacancies"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    enterprise_id: Mapped[int] = mapped_column(ForeignKey("enterprises.id"), nullable=False)
    area_id: Mapped[int] = mapped_column(ForeignKey("areas.id"), nullable=False)

    title: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    employment_type: Mapped[EmploymentTypeEnum] = mapped_column(Enum(EmploymentTypeEnum), nullable=False)
    experience_level: Mapped[ExperienceLevelEnum] = mapped_column(Enum(ExperienceLevelEnum), nullable=False)
    education_level: Mapped[EducationLevelEnum | None] = mapped_column(Enum(EducationLevelEnum), nullable=True)

    workplace_type: Mapped[WorkplaceTypeEnum] = mapped_column(Enum(WorkplaceTypeEnum), nullable=False)

    seniority: Mapped[int | None] = mapped_column(Integer, nullable=True)

    salary_min: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    salary_max: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    currency: Mapped[str | None] = mapped_column(String(10), nullable=True)

    requirements: Mapped[str | None] = mapped_column(String(300), nullable=True)
    responsibilities: Mapped[str | None] = mapped_column(String(300), nullable=True)
    benefits: Mapped[str | None] = mapped_column(String(300), nullable=True)

    status: Mapped[VacancyStatusEnum] = mapped_column(Enum(VacancyStatusEnum), default=VacancyStatusEnum.OPEN,
                                                      nullable=False)

    openings: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    application_deadline: Mapped[datetime | None] = mapped_column(Date, nullable=True)

    last_application_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                 onupdate=func.now(), nullable=False)

    enterprise: Mapped["EnterpriseEntity"] = relationship("EnterpriseEntity", back_populates="vacancies")
    area: Mapped["AreaEntity"] = relationship("AreaEntity", back_populates="vacancies")

    skills: Mapped[List["VacancySkillEntity"]] = relationship("VacancySkillEntity", back_populates="vacancy")
    applications: Mapped[List["ApplicationEntity"]] = relationship("ApplicationEntity", back_populates="vacancy")

    metrics: Mapped["VacancyMetricEntity"] = relationship(
        "VacancyMetricEntity",
        back_populates="vacancy",
        uselist=False,
        cascade="all, delete-orphan",
    )

class VacancyMetricEntity(Base):
    vacancy_id: Mapped[int] = mapped_column(
        ForeignKey("vacancies.id"), nullable=False, primary_key=True
    )

    shortlists_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    shares_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    vacancy: Mapped["VacancyEntity"] = relationship("VacancyEntity", back_populates="metrics")

    views_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    applications_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    interview_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                 onupdate=func.now(), nullable=False)
class VacancySkillEntity(Base):
    __tablename__ = "vacancy_skills"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    vacancy_id: Mapped[int] = mapped_column(ForeignKey("vacancies.id"), primary_key=True)
    skill_id: Mapped[int] = mapped_column(ForeignKey("skills.id"), primary_key=True)

    is_required: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    proficiency: Mapped[ProficiencyEnum | None] = mapped_column(Enum(ProficiencyEnum, name="proficiency_enum"),
                                                                nullable=True)
    years_experience: Mapped[int | None] = mapped_column(Integer, nullable=True)
    priority_level: Mapped[int | None] = mapped_column(Integer, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                 onupdate=func.now(), nullable=False)

    vacancy: Mapped["VacancyEntity"] = relationship("VacancyEntity", back_populates="skills")
    skill: Mapped["SkillEntity"] = relationship("SkillEntity", back_populates="vacancies")

class ApplicationEntity(Base):
    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    vacancy_id: Mapped[int] = mapped_column(ForeignKey("vacancies.id"), nullable=False)

    status: Mapped[ApplicationStatusEnum] = mapped_column(
        Enum(ApplicationStatusEnum, name="application_status_enum"),
        default=ApplicationStatusEnum.PENDING,
        nullable=False
    )

    is_viewed: Mapped[bool] = mapped_column(Boolean, default=False)
    priority_level: Mapped[int | None] = mapped_column(Integer, nullable=True)
    rating: Mapped[int | None] = mapped_column(Integer,
                                               nullable=True)
    feedback: Mapped[str | None] = mapped_column(Text, nullable=True)

    source: Mapped[ApplicationSourceEnum | None] = mapped_column(
        Enum(ApplicationSourceEnum, name="application_source_enum"),
        nullable=True
    )

    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    applied_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                 onupdate=func.now(), nullable=False)

    user: Mapped["UserEntity"] = relationship("UserEntity", back_populates="applications")
    vacancy: Mapped["VacancyEntity"] = relationship("VacancyEntity", back_populates="applications")

class EmployeeEnterpriseEntity(Base):
    __tablename__ = "employees_enterprise"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    enterprise_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("enterprises.id"))

    position: Mapped[str | None] = mapped_column(String(100), nullable=True)
    salary_range: Mapped[str | None] = mapped_column(String(100), nullable=True)

    employment_type: Mapped[EmploymentTypeEnum] = mapped_column(
        Enum(EmploymentTypeEnum, name="employment_type_enum"), nullable=False
    )

    employment_status: Mapped[EmploymentStatusEnum] = mapped_column(
        Enum(EmploymentStatusEnum, name="employment_status_enum"), nullable=False
    )

    start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                 onupdate=func.now(), nullable=False)

    owner: Mapped["UserEntity"] = relationship("UserEntity", back_populates="employments")
    enterprise: Mapped["EnterpriseEntity"] = relationship("EnterpriseEntity", back_populates="employments")

class ReviewEnterprise(Base):
    __tablename__ = "reviews_enterprise"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)

    title: Mapped[str] = mapped_column(String(80), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    pros: Mapped[str | None] = mapped_column(String(400), nullable=True)
    cons: Mapped[str | None] = mapped_column(String(400), nullable=True)

    would_recommend: Mapped[bool] = mapped_column(Boolean, default=True)

    position: Mapped[str | None] = mapped_column(String(100), nullable=True)
    salary_range: Mapped[str | None] = mapped_column(String(100), nullable=True)

    employment_type: Mapped[EmploymentTypeEnum] = mapped_column(
        Enum(EmploymentTypeEnum, name="employment_type_enum"), nullable=False
    )

    employment_status: Mapped[EmploymentStatusEnum] = mapped_column(
        Enum(EmploymentStatusEnum, name="employment_status_enum"), nullable=False
    )

    helpful_votes: Mapped[int] = mapped_column(Integer, default=0)
    unhelpful_votes: Mapped[int] = mapped_column(Integer, default=0)

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    enterprise_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("enterprises.id"))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                 onupdate=func.now(), nullable=False)

    owner: Mapped["UserEntity"] = relationship("UserEntity", back_populates="reviews")
    enterprise: Mapped["EnterpriseEntity"] = relationship("EnterpriseEntity", back_populates="reviews")

class PostEnterpriseEntity(Base):
    __tablename__ = "posts_enterprise"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    url_image: Mapped[str | None] = mapped_column(Text, nullable=True)

    enterprise_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("enterprises.id"))
    category_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("categories.id"))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                 onupdate=func.now(), nullable=False)

    enterprise: Mapped["EnterpriseEntity"] = relationship("EnterpriseEntity", back_populates="posts")
    category: Mapped["CategoryEntity"] = relationship("CategoryEntity", back_populates="posts_enterprise")
    favorite_post_enterprise: Mapped[list["FavoritePostEnterpriseEntity"]] = relationship(
        "FavoritePostEnterpriseEntity", back_populates="posts")

    reactions: Mapped[List["ReactionPostEnterpriseEntity"]] = relationship(
        "ReactionPostEnterpriseEntity",
        back_populates="post_enterprise",
        cascade="all, delete-orphan"
    )

    comments: Mapped[List["CommentPostEnterpriseEntity"]] = relationship(
        "CommentPostEnterpriseEntity",
        back_populates="post",
        cascade="all, delete-orphan",
    )

class CommentPostEnterpriseEntity(Base):
    __tablename__ = "comments_posts_enterprise"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    content: Mapped[str] = mapped_column(Text, nullable=False)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    post_enterprise_id: Mapped[int] = mapped_column(
        ForeignKey("posts_enterprise.id", ondelete="CASCADE"), nullable=False
    )

    parent_comment_id: Mapped[int | None] = mapped_column(
        ForeignKey("comments_posts_enterprise.id", ondelete="CASCADE"), nullable=True
    )

    is_edited: Mapped[bool] = mapped_column(Boolean, default=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)

    user: Mapped["UserEntity"] = relationship(
        "UserEntity",
        back_populates="enterprise_post_comments",
        lazy="joined"
    )

    post: Mapped["PostEnterpriseEntity"] = relationship(
        "PostEnterpriseEntity",
        back_populates="comments",
        lazy="joined"
    )

    parent: Mapped["CommentPostEnterpriseEntity"] = relationship(
        "CommentPostEnterpriseEntity",
        remote_side=[id],
        back_populates="replies"
    )

    replies: Mapped[List["CommentPostEnterpriseEntity"]] = relationship(
        "CommentPostEnterpriseEntity",
        back_populates="parent"
    )

    favorites: Mapped[list["FavoriteCommentPostEnterpriseEntity"]] = relationship(
        "FavoriteCommentPostEnterpriseEntity",
        back_populates="comment",
        cascade="all, delete-orphan"
    )

    reactions: Mapped[list["ReactionCommentPostEnterpriseEntity"]] = relationship(
        "ReactionCommentPostEnterpriseEntity",
        back_populates="comment",
        cascade="all, delete-orphan"
    )

class ReactionCommentPostEnterpriseEntity(Base):
    __tablename__ = "reaction_comments_enterprise"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    __table_args__ = (
        UniqueConstraint('user_id', 'comment_enterprise_id', name='_user_comment_enterprise_uc'),
    )

    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id"), nullable=False
    )

    comment_enterprise_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("comments_posts_enterprise.id"), nullable=False
    )

    reaction_type: Mapped[ReactionTypeEnum] = mapped_column(
        Enum(ReactionTypeEnum, name="reaction_type_enum"), nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    user: Mapped["UserEntity"] = relationship(
        "UserEntity",
        foreign_keys=[user_id],
        back_populates="comment_enterprise_reactions",
        lazy="joined"
    )

    comment: Mapped["CommentPostEnterpriseEntity"] = relationship(
        "CommentPostEnterpriseEntity",
        foreign_keys=[comment_enterprise_id],
        back_populates="reactions",
        lazy="joined"
    )

class FavoriteCommentPostEnterpriseEntity(Base):
    __tablename__ = "favorite_comments_enterprise"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=False)
    comment_enterprise_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("comments_posts_enterprise.id"),
                                                       nullable=False)

    __table_args__ = (
        UniqueConstraint("user_id", "comment_enterprise_id", name="uq_user_comment_favorite"),
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    user: Mapped["UserEntity"] = relationship(
        "UserEntity",
        back_populates="favorite_comment_enterprise"
    )

    comment: Mapped["CommentPostEnterpriseEntity"] = relationship(
        "CommentPostEnterpriseEntity", back_populates="favorites"
    )

class ReactionPostEnterpriseEntity(Base):
    __tablename__ = "reaction_posts_enterprise"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    __table_args__ = (
        UniqueConstraint('user_id', 'post_enterprise_id', name='_user_post_enterprise_uc'),
    )

    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id")
    )

    post_enterprise_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("posts_enterprise.id")
    )

    reaction_type: Mapped[ReactionTypeEnum] = mapped_column(
        Enum(ReactionTypeEnum, name="reaction_type_enum"), nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    user: Mapped["UserEntity"] = relationship(
        "UserEntity",
        foreign_keys=[user_id],
        back_populates="enterprise_post_reactions"
    )

    post_enterprise: Mapped["PostEnterpriseEntity"] = relationship(
        "PostEnterpriseEntity",
        foreign_keys=[post_enterprise_id],
        back_populates="reactions"
    )

class FavoritePostEnterpriseEntity(Base):
    __tablename__ = "favorite_posts_enterprise"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    post_enterprise_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("posts_enterprise.id"))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    owner: Mapped["UserEntity"] = relationship("UserEntity", back_populates="favorite_post_enterprise")
    posts: Mapped["PostEnterpriseEntity"] = relationship("PostEnterpriseEntity",
                                                         back_populates="favorite_post_enterprise")

class CategoryEntity(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    slug: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    order: Mapped[int] = mapped_column(Integer, default=0)

    post_count: Mapped[int] = mapped_column(Integer, default=0)
    job_count: Mapped[int] = mapped_column(Integer, default=0)

    icon_url: Mapped[str | None] = mapped_column(String(255), nullable=True)

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    parent_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("categories.id"), nullable=True)
    children: Mapped[list["CategoryEntity"]] = relationship("CategoryEntity", backref="parent",
                                                            remote_side="CategoryEntity.id")

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)

    owner: Mapped["UserEntity"] = relationship("UserEntity", back_populates="categories")
    posts: Mapped[list["PostUserEntity"]] = relationship("PostUserEntity", back_populates="category")
    posts_enterprise: Mapped[list["PostEnterpriseEntity"]] = relationship("PostEnterpriseEntity",
                                                                          back_populates="category")

class PostUserEntity(Base):
    __tablename__ = "posts_user"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    url_image: Mapped[str | None] = mapped_column(Text, nullable=True)

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    category_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("categories.id"))

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)

    owner: Mapped["UserEntity"] = relationship("UserEntity", back_populates="posts")
    category: Mapped["CategoryEntity"] = relationship("CategoryEntity", back_populates="posts")

    favorite_post_user: Mapped[list["FavoritePostUserEntity"]] = relationship("FavoritePostUserEntity",
                                                                              back_populates="post_user")
    medias: Mapped[list["MediaPostUserEntity"]] = relationship("MediaPostUserEntity", back_populates="post")

    reactions: Mapped[List["ReactionPostUserEntity"]] = relationship(
        "ReactionPostUserEntity",
        back_populates="post",
        cascade="all, delete-orphan"
    )

    comments: Mapped[list["CommentPostUserEntity"]] = relationship(
        "CommentPostUserEntity",
        back_populates="post",
        cascade="all, delete-orphan",
    )

class CommentPostUserEntity(Base):
    __tablename__ = "comments_posts_user"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    content: Mapped[str] = mapped_column(Text, nullable=False)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    post_user_id: Mapped[int] = mapped_column(
        ForeignKey("posts_user.id", ondelete="CASCADE"), nullable=False
    )

    parent_comment_id: Mapped[int | None] = mapped_column(
        ForeignKey("comments_posts_user.id", ondelete="CASCADE"), nullable=True
    )

    is_edited: Mapped[bool] = mapped_column(Boolean, default=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)

    user: Mapped["UserEntity"] = relationship("UserEntity", back_populates="comments", lazy="joined")

    post: Mapped["PostUserEntity"] = relationship("PostUserEntity", back_populates="comments", lazy="joined")

    parent: Mapped["CommentPostUserEntity"] = relationship(
        "CommentPostUserEntity",
        remote_side=[id],
        back_populates="replies"
    )

    replies: Mapped[List["CommentPostUserEntity"]] = relationship(
        "CommentPostUserEntity",
        back_populates="parent"
    )

    favorites: Mapped[List["FavoriteCommentPostUserEntity"]] = relationship(
        "FavoriteCommentPostUserEntity",
        back_populates="comment",
        cascade="all, delete-orphan"
    )

    reactions: Mapped[List["ReactionCommentPostUserEntity"]] = relationship(
        "ReactionCommentPostUserEntity",
        back_populates="comment",
        cascade="all, delete-orphan",
    )

class ReactionCommentPostUserEntity(Base):
    __tablename__ = "reaction_comments_user"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    __table_args__ = (
        UniqueConstraint('user_id', 'comment_user_id', name='_user_comment_user_uc'),
    )

    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id")
    )
    comment_user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("comments_posts_user.id")
    )

    reaction_type: Mapped[ReactionTypeEnum] = mapped_column(
        Enum(ReactionTypeEnum, name="reaction_type_enum"), nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    user: Mapped["UserEntity"] = relationship(
        "UserEntity",
        foreign_keys=[user_id],
        back_populates="comment_user_reactions",
        lazy="joined"
    )

    comment: Mapped["CommentPostUserEntity"] = relationship(
        "CommentPostUserEntity",
        foreign_keys=[comment_user_id],
        back_populates="reactions",
        lazy="joined"
    )

class FavoriteCommentPostUserEntity(Base):
    __tablename__ = "favorite_comments_user"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=False)
    comment_user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("comments_posts_user.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint("user_id", "comment_user_id", name="uq_user_comment_user_favorite"),
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    user: Mapped["UserEntity"] = relationship(
        "UserEntity",
        back_populates="favorite_comment_user"
    )

    comment: Mapped["CommentPostUserEntity"] = relationship(
        "CommentPostUserEntity", back_populates="favorites"
    )

class ReactionPostUserEntity(Base):
    __tablename__ = "reaction_posts_user"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    __table_args__ = (
        UniqueConstraint('user_id', 'post_user_id', name='_user_post_uc'),
    )

    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id")
    )
    post_user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("posts_user.id")
    )

    reaction_type: Mapped[ReactionTypeEnum] = mapped_column(
        Enum(ReactionTypeEnum, name="reaction_type_enum"), nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    user: Mapped["UserEntity"] = relationship(
        "UserEntity",
        foreign_keys=[user_id],
        back_populates="post_reactions"
    )

    post: Mapped["PostUserEntity"] = relationship(
        "PostUserEntity",
        foreign_keys=[post_user_id],
        back_populates="reactions"
    )

class MediaPostUserEntity(Base):
    __tablename__ = "medias_post_user"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    url: Mapped[str] = mapped_column(String(800), nullable=False, index=True)
    type: Mapped[MediaType] = mapped_column(Enum(MediaType, name="media_type"), nullable=False)
    order: Mapped[int] = mapped_column(Integer, default=0)
    caption: Mapped[str | None] = mapped_column(String(255), nullable=True)
    size: Mapped[int | None] = mapped_column(Integer, nullable=True)
    mime_type: Mapped[str | None] = mapped_column(String(100), nullable=True)

    post_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("posts_user.id"))

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)

    post: Mapped["PostUserEntity"] = relationship("PostUserEntity", back_populates="medias")

class FavoritePostUserEntity(Base):
    __tablename__ = "favorite_posts_user"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))

    post_user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("posts_user.id"))

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    owner: Mapped["UserEntity"] = relationship("UserEntity", back_populates="favorite_post_user")
    post_user: Mapped["PostUserEntity"] = relationship("PostUserEntity", back_populates="favorite_post_user")
