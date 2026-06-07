from fastapi import APIRouter
from ..schemas import PostCreate, PostUpdate, PostResponse
from ..crud import posts as p

router = APIRouter()

# get all the posts for the homepage
@router.get('/posts')
async def get_posts() -> list[PostResponse]:
  return p.get_posts()

@router.post('/posts')
async def create_post(post: PostCreate) -> dict:
  return p.create_post(post)

# update a post
@router.put('/posts/{post_id}')
async def update_post(post_id: int, post: PostUpdate) -> dict:
  return p.update_post(post_id, post)

# delete a post
@router.delete('/posts/{post_id}')
async def delete_post(post_id: int) -> dict:
  return p.delete_post(post_id)