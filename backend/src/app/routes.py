from fastapi import APIRouter
from .schemas import SectionResponse, FolderResponse, PostResponse, PostCreate
from . import crud

router = APIRouter()

# get all the sections
@router.get('/sections')
async def get_sections() -> list[SectionResponse]:
  return crud.get_sections()

# get all folders
@router.get('/folders')
async def get_folders() -> list[FolderResponse]:
  return crud.get_folders()

# get all the posts for the homepage
@router.get('/posts')
async def get_posts() -> list[PostResponse]:
  return crud.get_posts()

# create a post (type hint auto validates input using pydantic model)
@router.post('/posts')
async def create_post(post: PostCreate) -> dict:
  return crud.create_post(post)