from sqlalchemy import (
    Column,
    ForeignKey,
    ForeignKeyConstraint,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from database import Base


class Work(Base):
    __tablename__ = "work"

    id = Column(String(32), nullable=False, primary_key=True)
    title = Column(String(32), nullable=False)
    long_title = Column(String(64), nullable=False)
    year = Column(Integer, nullable=False)
    genre_type = Column(String(1), nullable=False)
    notes = Column(Text, nullable=True)
    source = Column(String(16), nullable=False)
    total_words = Column(Integer, nullable=False)
    total_paragraphs = Column(Integer, nullable=False)

    chapters = relationship("Chapter")
    characters = relationship(
        "Character",
        secondary="character_work",
        back_populates="works",
    )

    def __repr__(self) -> str:
        return self._repr(
            id=self.id,
            title=self.title,
        )


class Chapter(Base):
    __tablename__ = "chapter"
    __table_args__ = (
        UniqueConstraint("work_id", "section_number", "chapter_number"),
    )

    index = Column(
        Integer, nullable=False, primary_key=True, autoincrement=True
    )

    chapter_number = Column(Integer, nullable=False)
    section_number = Column(Integer, nullable=False)
    work_id = Column(String(32), ForeignKey("work.id"), nullable=False)

    description = Column(String(256), nullable=False)

    paragraphs = relationship("Paragraph")

    def __repr__(self) -> str:
        return self._repr(
            index=self.index,
            work_id=self.work_id,
            chapter_number=self.chapter_number,
            section_number=self.section_number,
        )


class Paragraph(Base):
    __tablename__ = "paragraph"
    __table_args__ = (
        ForeignKeyConstraint(
            ["work_id", "section_number", "chapter_number"],
            [
                "chapter.work_id",
                "chapter.section_number",
                "chapter.chapter_number",
            ],
        ),
    )

    index = Column(
        Integer, nullable=False, primary_key=True, autoincrement=True
    )

    work_id = Column(String(32), ForeignKey("work.id"), nullable=False)
    section_number = Column(Integer, nullable=False)
    chapter_number = Column(Integer, nullable=False)

    character_id = Column(
        String(32),
        ForeignKey("character.id"),
        nullable=False,
    )
    character = relationship("Character", foreign_keys=[character_id])

    paragraph_num = Column(Integer, nullable=False)
    paragraph_type = Column(String(1), nullable=False)

    plain_text = Column(Text, nullable=False)
    phonetic_text = Column(Text, nullable=False)
    stem_text = Column(Text, nullable=False)

    char_count = Column(Integer, nullable=False)
    word_count = Column(Integer, nullable=False)

    def __repr__(self) -> str:
        return self._repr(
            index=self.index,
            work_id=self.work_id,
            chapter_number=self.chapter_number,
            section_number=self.section_number,
        )


class Character(Base):
    __tablename__ = "character"

    id = Column(String(32), nullable=False, primary_key=True)
    name = Column(String(64), nullable=False)
    abbrev = Column(String(32), nullable=True)
    description = Column(String(2056), nullable=True)
    speech_count = Column(Integer, nullable=False)

    works = relationship(
        "Work",
        secondary="character_work",
        back_populates="characters",
    )

    def __repr__(self) -> str:
        return self._repr(
            id=self.id,
            name=self.name,
        )


class CharacterWork(Base):
    """Assosication table for Character -> Works many to many relationship."""

    __tablename__ = "character_work"

    character_id = Column(
        String(32),
        ForeignKey("character.id"),
        nullable=False,
        primary_key=True,
    )
    work_id = Column(
        String(32),
        ForeignKey("work.id"),
        nullable=False,
        primary_key=True,
    )


class Wordform(Base):
    __tablename__ = "wordform"

    index = Column(
        Integer,
        nullable=False,
        primary_key=True,
        autoincrement=True,
    )
    plain_text = Column(Text, nullable=False)
    phonetic_text = Column(Text, nullable=False)
    stem_text = Column(Text, nullable=False)
    occurences = Column(Integer, nullable=False)

    def __repr__(self) -> str:
        return self._repr(
            index=self.index,
            plain_text=self.plain_text,
        )
