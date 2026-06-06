from fastapi import APIRouter
from .schemas import SectionResponse, FolderResponse, PostResponse, PostCreate, PostUpdate, FolderCreate, NoteCreate, NoteResponse, NoteUpdate, VoteCreate
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

# update a post
@router.put('/posts/{post_id}')
async def update_post(post_id: int, post: PostUpdate) -> dict:
  return crud.update_post(post_id, post)

# delete a post
@router.delete('/posts/{post_id}')
async def delete_post(post_id: int) -> dict:
  return crud.delete_post(post_id)

# create a folder
@router.post('/folders')
async def create_folder(folder: FolderCreate) -> dict:
  return crud.create_folder(folder)

# update a folder
@router.put('/folders/{folder_id}')
async def update_folder(folder_id: int, folder: FolderCreate) -> dict:
  return crud.update_folder(folder_id, folder)

# delete a folder
@router.delete('/folders/{folder_id}')
async def delete_folder(folder_id: int) -> dict:
  return crud.delete_folder(folder_id)

# create a private note
@router.post('/notes')
async def create_note(note: NoteCreate) -> dict:
  return crud.create_note(note)

# update a private note
@router.put('/notes/{note_id}')
async def update_note(note_id: int, note: NoteUpdate) -> dict:
  return crud.update_note(note_id, note)

# delete a private note
@router.delete('/notes/{note_id}')
async def delete_note(note_id: int) -> dict:
  return crud.delete_note(note_id)

# get a private note
@router.get('/notes/{post_id}')
async def get_notes(post_id: int) -> list[NoteResponse]:
  return crud.get_notes(post_id)

# get user's vote on a post
@router.get('/votes/{post_id}')
async def get_votes(post_id: int) -> dict | None:
  return crud.get_votes(post_id)

# Total votes on a post
@router.get('/posts/{post_id}/votes')
async def get_post_votes(post_id: int) -> dict:
  return crud.get_post_votes(post_id)

# Create a vote
@router.post('/votes')
async def create_vote(vote: VoteCreate) -> dict:
  return crud.create_vote(vote)

# Update a vote
@router.put('/votes/{post_id}')
async def update_vote(post_id: int, vote: VoteCreate) -> dict:
  return crud.update_vote(post_id, vote)

# Delete a vote
@router.delete('/votes/{post_id}')
async def delete_vote(post_id: int) -> dict:
  return crud.delete_vote(post_id)

@router.post('/saved-posts/{post_id}')
async def save_post(post_id: int) -> dict:
  return crud.save_post(post_id)

@router.delete('/saved-posts/{post_id}')
async def unsave_post(post_id: int) -> dict:
  return crud.unsave_post(post_id)

@router.get('/saved-posts')
async def get_saved_posts() -> list:
  return crud.get_saved_posts()