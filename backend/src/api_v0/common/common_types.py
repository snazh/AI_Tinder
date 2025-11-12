from typing import Union, TypeVar
from src.database.models import Base
from pydantic import BaseModel

ColumnValue = Union[str, int, bool]
ModelType = TypeVar("ModelType", bound=Base)
SchemaType = TypeVar("SchemaType", bound=BaseModel)
