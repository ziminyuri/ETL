from pydantic import BaseModel
from typing import Union, Optional, List, Dict
from uuid import UUID

OBJ_ID = Union[UUID, str]
OBJ_NAME = Union[str, str]


class Film(BaseModel):
    id: Union[int, str, UUID]
    title: str
    description: str
    imdb_rating: str
    # genre: List[Dict[OBJ_ID, OBJ_NAME]]
    genre: str
    actors_names: List[str] = None
    writers_names: List[str] = None
    director: Dict[OBJ_ID, OBJ_NAME] = None
    actors: List[Dict[OBJ_ID, OBJ_NAME]] = None
    writers: List[Dict[OBJ_ID, OBJ_NAME]] = None




