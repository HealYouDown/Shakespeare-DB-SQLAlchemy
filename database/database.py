from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

fpath = "./shakespeare.db"
sqlalchemy_url = f"sqlite:///{fpath}"

engine = create_engine(
    sqlalchemy_url,
    encoding="utf-8",
)
session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )
)
