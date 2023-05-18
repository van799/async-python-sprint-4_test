from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from short_link_api.models.database_init import Database

database = Database()
router = APIRouter()

@router.get("/")
def read_entities(
        db: AsyncSession = Depends(database.get_session)) -> Any:
    """
    Retrieve entities.
    """
    entities = {"a": 1}
    # get entities from db
    return entities
