from fastapi import APIRouter
from ..crud import saved_posts as sp

router = APIRouter()

# save a post
@router.post('/saved-posts/{post_id}')
async def save_post(post_id: int) -> dict:
  return sp.save_post(post_id)

# unsave a post
@router.delete('/saved-posts/{post_id}')
async def unsave_post(post_id: int) -> dict:
  return sp.unsave_post(post_id)

# get saved posts
@router.get('/saved-posts')
async def get_saved_posts() -> list:
  return sp.get_saved_posts()