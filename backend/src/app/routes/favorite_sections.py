from fastapi import APIRouter
from ..crud import favorite_sections as fs

router = APIRouter()

# mark a section favorite
@router.post('/favorite-sections/{section_id}')
async def favorite_section(section_id: int) -> dict:
  return fs.favorite_section(section_id)

# unmark a section as favorite
@router.delete('/favorite-sections/{section_id}')
async def unfavorite_section(section_id: int) -> dict:
  return fs.unfavorite_section(section_id)

# get all favorite sections
@router.get('/favorite-sections')
async def get_favorite_sections() -> list:
  return fs.get_favorite_sections()