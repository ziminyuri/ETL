from typing import Dict, List, Union
from uuid import UUID

from pydantic import BaseModel

OBJ_ID = Union[UUID, str]
OBJ_NAME = Union[str, str]


class Film(BaseModel):
    id: Union[int, str, UUID]
    title: str
    description: str = ''
    imdb_rating: str
    genre: List[str]
    actors_names: List[str]
    writers_names: List[str]
    director: List[str]
    actors: List[Dict[OBJ_ID, OBJ_NAME]] = None
    writers: List[Dict[OBJ_ID, OBJ_NAME]] = None




