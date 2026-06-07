from fastapi import APIRouter
from ..schemas import SectionResponse
from ..crud import sections as s

router = APIRouter()

# get all the sections
@router.get('/sections')
async def get_sections() -> list[SectionResponse]:
  return s.get_sections()