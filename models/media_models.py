from beanie import Document
from datetime import datetime
from pydantic import BaseModel, Extra
from typing import Optional
from enum import StrEnum, auto


class NewsSource(StrEnum):
    GUARDIAN = auto()
    INDEPENDENT = auto()
    LATIMES = auto()
    SMH = auto()


class TheGuardian(Document):

    article_title: Optional[str] | None = None
    summary: Optional[str] | None = None
    author: Optional[str] | None = None
    date_of_pub: Optional[datetime] | None = None
    content: Optional[str] | None = None
    url: Optional[str] | None = None

    class Settings:
        name = "the_guardian"

    class Config:
        extra = Extra.allow
        schema_extra = {
            "article_title": "As Russia’s armed forces fight among themselves, it’s hard to know who’s in control",  # noqa: E501
            "summary": "Wagner group chief Yevgeny Prigozhin has launched another diatribe against the Russian army. Is he a loose cannon, or a Kremlin puppet?",  # noqa: E501
            "author": "Samantha de Bendern",
            "date_of_pub": "9 Jun 2023",
            "content": "Coming just a day before the world’s media became ... ",
            "url": "https://www.theguardian.com/commentisfree/2023/jun/09/russian-armed-forces-infighting-yevgeny-prigozhin",
        }


class Independent(Document):

    article_title: Optional[str] | None = None
    summary: Optional[str] | None = None
    author: Optional[str] | None = None
    date_of_pub: Optional[datetime] | None = None
    content: Optional[str] | None = None
    url: Optional[str] | None = None

    class Settings:
        name = "independent"

    class Config:
        extra = Extra.allow
        schema_extra = {
            "article_title": "As Russia’s armed forces fight among themselves, it’s hard to know who’s in control",  # noqa: E501
            "summary": "Wagner group chief Yevgeny Prigozhin has launched another diatribe against the Russian army. Is he a loose cannon, or a Kremlin puppet?",  # noqa: E501
            "author": "Samantha de Bendern",
            "date_of_pub": "9 Jun 2023",
            "content": "Coming just a day before the world’s media became ... ",
            "url": "https://www.theguardian.com/commentisfree/2023/jun/09/russian-armed-forces-infighting-yevgeny-prigozhin",
        }


class LATimes(Document):

    article_title: Optional[str] | None = None
    summary: Optional[str] | None = None
    author: Optional[str] | None = None
    date_of_pub: Optional[datetime] | None = None
    content: Optional[str] | None = None
    url: Optional[str] | None = None

    class Settings:
        name = "la_times"

    class Config:
        extra = Extra.allow
        schema_extra = {
            "article_title": "As Russia’s armed forces fight among themselves, it’s hard to know who’s in control",  # noqa: E501
            "summary": "Wagner group chief Yevgeny Prigozhin has launched another diatribe against the Russian army. Is he a loose cannon, or a Kremlin puppet?",  # noqa: E501
            "author": "Samantha de Bendern",
            "date_of_pub": "9 Jun 2023",
            "content": "Coming just a day before the world’s media became ... ",
            "url": "https://www.theguardian.com/commentisfree/2023/jun/09/russian-armed-forces-infighting-yevgeny-prigozhin",
        }


class SMH(Document):

    article_title: Optional[str] | None = None
    summary: Optional[str] | None = None
    author: Optional[str] | None = None
    date_of_pub: Optional[datetime] | None = None
    content: Optional[str] | None = None
    url: Optional[str] | None = None

    class Settings:
        name = "sydney_morning_herald"

    class Config:
        extra = Extra.allow
        schema_extra = {
            "article_title": "As Russia’s armed forces fight among themselves, it’s hard to know who’s in control",  # noqa: E501
            "summary": "Wagner group chief Yevgeny Prigozhin has launched another diatribe against the Russian army. Is he a loose cannon, or a Kremlin puppet?",  # noqa: E501
            "author": "Samantha de Bendern",
            "date_of_pub": "9 Jun 2023",
            "content": "Coming just a day before the world’s media became ... ",
            "url": "https://www.theguardian.com/commentisfree/2023/jun/09/russian-armed-forces-infighting-yevgeny-prigozhin",
        }


print(NewsSource.GUARDIAN)
