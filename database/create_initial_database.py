import json
import os
from typing import Dict, List

from .base import Base
from .database import engine, session
from .models import Chapter, Character, Paragraph, Wordform, Work


def load_data(fname: str) -> List[dict]:
    with open(os.path.join(".", "database", "data", fname), "r") as fp:
        return json.load(fp)


def create_database():
    Base.metadata.create_all(engine)

    works = load_data("work.json")
    wordforms = load_data("wordform.json")
    characters = load_data("character.json")

    character_objs: Dict[str, Character] = {
        character["id"]: Character(
            id=character["id"],
            description=character["description"],
            abbrev=character["abbrev"],
            name=character["name"],
            speech_count=character["speech_count"],
        )
        for character in characters
    }
    session.add_all(character_objs.values())

    session.add_all(
        [
            Wordform(
                phonetic_text=wordform["phonetic_text"],
                plain_text=wordform["plain_text"],
                stem_text=wordform["stem_text"],
                occurences=wordform["occurences"],
            )
            for wordform in wordforms
        ]
    )

    for work in works:
        work_obj = Work(
            id=work["id"],
            title=work["title"],
            long_title=work["long_title"],
            year=work["year"],
            genre_type=work["genre_type"],
            notes=work["notes"],
            source=work["source"],
            total_words=work["total_words"],
            total_paragraphs=work["total_paragraphs"],
        )
        work_obj.characters = [
            character
            for character_id, character in character_objs.items()
            if character_id in work["character_ids"]
        ]

        for chapter in work["chapters"]:
            chapter_obj = Chapter(
                chapter_number=chapter["chapter_number"],
                section_number=chapter["section_number"],
                description=chapter["description"],
            )
            work_obj.chapters.append(chapter_obj)

            for paragraph in chapter["paragraphs"]:
                paragraph_obj = Paragraph(
                    character_id=paragraph["character_id"],
                    paragraph_num=paragraph["paragraph_num"],
                    paragraph_type=paragraph["paragraph_type"],
                    plain_text=paragraph["plain_text"],
                    phonetic_text=paragraph["phonetic_text"],
                    stem_text=paragraph["stem_text"],
                    char_count=paragraph["char_count"],
                    word_count=paragraph["word_count"],
                )
                chapter_obj.paragraphs.append(paragraph_obj)

        session.add(work_obj)

    session.commit()
