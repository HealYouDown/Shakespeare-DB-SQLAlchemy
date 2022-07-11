# Shakespeare-Database in SQLAlchemy
Implements the open available database for shakespeare's works ([OSS](https://www.opensourceshakespeare.org/)) in SQLAlchemy.

## Schema
![](./docs/schema.svg)

## Running
Obviously, to run any queries, you need to have SQLAlchemy (`pip install sqlalchemy`) installed.

### Queries
You can write queries in the `main.py` file.

When executing the file, it will check if the database `shakespeare.db` exists in the root directory. If it does not, it will be created and filled automatically.
