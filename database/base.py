from sqlalchemy.ext.declarative import declarative_base

Base_ = declarative_base()


class Base(Base_):
    __abstract__ = True

    def _repr(self, **fields) -> str:
        model_name = self.__class__.__name__

        fields = [f"{key}={repr(value)}" for key, value in fields.items()]

        if fields:
            return f"<{model_name} {', '.join(fields)}>"

        return f"<{model_name} {id(self)}>"
