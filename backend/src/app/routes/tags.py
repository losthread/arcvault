from fastapi import APIRouter
from ..schemas import TagCreate, TagResponse
from ..crud import tags as t

router = APIRouter()

# get tags
@router.get('/tags')
async def get_tags() -> list[TagResponse]:
  return t.get_tags()

# get tags on a post
@router.get('/posts/{post_id}/tags')
async def get_post_tags(post_id: int) -> list[TagResponse]:
  return t.get_post_tags(post_id)

# create a tag
@router.post('/tags')
async def create_tag(tag: TagCreate) -> dict:
  return t.create_tag(tag.name)

# create a tag on a post
@router.post('/posts/{post_id}/tags/{tag_id}')
async def add_tag(post_id: int, tag_id: int) -> dict:
  return t.add_tag_to_post(post_id, tag_id)

# remove a tag from a post
@router.delete('/posts/{post_id}/tags/{tag_id}')
async def remove_tag(post_id: int, tag_id: int) -> dict:
  return t.remove_tag_from_post(post_id, tag_id)