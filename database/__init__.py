from .base import Base
from .create_initial_database import create_database
from .database import engine, fpath, session
from .models import Chapter, Character, Paragraph, Wordform, Work

__all__ = [
    "Base",
    "engine",
    "session",
    "Work",
    "Character",
    "Paragraph",
    "Chapter",
    "Wordform",
]

import os

# Create database if it does not exist yet
# Will also fill the database with all needed data.
if not os.path.exists(fpath):
    create_database()
