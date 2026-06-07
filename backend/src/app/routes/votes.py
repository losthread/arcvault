from fastapi import APIRouter
from ..schemas import VoteCreate
from ..crud import tags as t

router = APIRouter()

# get user's vote on a post
@router.get('/votes/{post_id}')
async def get_votes(post_id: int) -> dict | None:
  return t.get_votes(post_id)

# Total votes on a post
@router.get('/posts/{post_id}/votes')
async def get_post_votes(post_id: int) -> dict:
  return t.get_post_votes(post_id)

# Create a vote
@router.post('/votes')
async def create_vote(vote: VoteCreate) -> dict:
  return t.create_vote(vote)

# Update a vote
@router.put('/votes/{post_id}')
async def update_vote(post_id: int, vote: VoteCreate) -> dict:
  return t.update_vote(post_id, vote)

# Delete a vote
@router.delete('/votes/{post_id}')
async def delete_vote(post_id: int) -> dict:
  return t.delete_vote(post_id)