# Generates structured json files from original database dumps

import json
import os


def obj_with_keys(obj: dict, keys: list[str]) -> dict:
    return {key: value for key, value in obj.items() if key in keys}


if __name__ == "__main__":
    data_path = os.path.join(".", "og", "db_dump")
    save_path = os.path.join(".", "database", "data")

    data = {}
    for key in [
        "chapter",
        "character_work",
        "character",
        "paragraph",
        "wordform",
        "work",
    ]:
        with open(os.path.join(data_path, f"{key}.json"), "r") as fp:
            data[key] = json.load(fp)

    for work in data["work"]:
        del work["index"]

        work["character_ids"] = [
            cw["character_id"]
            for cw in data["character_work"]
            if cw["work_id"] == work["id"]
        ]

        work["chapters"] = [
            obj_with_keys(
                c, ["chapter_number", "description", "section_number"]
            )
            for c in data["chapter"]
            if c["work_id"] == work["id"]
        ]
        for chapter in work["chapters"]:
            chapter["paragraphs"] = [
                obj_with_keys(
                    p,
                    [
                        "char_count",
                        "character_id",
                        "paragraph_num",
                        "paragraph_type",
                        "phonetic_text",
                        "plain_text",
                        "stem_text",
                        "word_count",
                    ],
                )
                for p in data["paragraph"]
                if p["work_id"] == work["id"]
                and p["chapter_number"] == chapter["chapter_number"]
                and p["section_number"] == chapter["section_number"]
            ]

    with open(os.path.join(save_path, "work.json"), "w") as fp:
        json.dump(data["work"], fp)

    with open(os.path.join(save_path, "wordform.json"), "w") as fp:
        for workform in data["wordform"]:
            del workform["id"]
            del workform["index"]

        json.dump(data["wordform"], fp)

    with open(os.path.join(save_path, "character.json"), "w") as fp:
        for character in data["character"]:
            del character["index"]

        json.dump(data["character"], fp)
