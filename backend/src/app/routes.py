from fastapi import APIRouter
from .schemas import SectionResponse, FolderResponse, PostResponse, PostCreate, PostUpdate, FolderCreate, NoteCreate, NoteResponse, NoteUpdate, VoteCreate, TagResponse, TagCreate, ReportCreate
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

# save a post
@router.post('/saved-posts/{post_id}')
async def save_post(post_id: int) -> dict:
  return crud.save_post(post_id)

# unsave a post
@router.delete('/saved-posts/{post_id}')
async def unsave_post(post_id: int) -> dict:
  return crud.unsave_post(post_id)

# get saved posts
@router.get('/saved-posts')
async def get_saved_posts() -> list:
  return crud.get_saved_posts()

# mark a section favorite
@router.post('/favorite-sections/{section_id}')
async def favorite_section(section_id: int) -> dict:
  return crud.favorite_section(section_id)

# unmark a section as favorite
@router.delete('/favorite-sections/{section_id}')
async def unfavorite_section(section_id: int) -> dict:
  return crud.unfavorite_section(section_id)

# get all favorite sections
@router.get('/favorite-sections')
async def get_favorite_sections() -> list:
  return crud.get_favorite_sections()

# get tags
@router.get('/tags')
async def get_tags() -> list[TagResponse]:
  return crud.get_tags()

# get tags on a post
@router.get('/posts/{post_id}/tags')
async def get_post_tags(post_id: int) -> list[TagResponse]:
  return crud.get_post_tags(post_id)

# create a tag
@router.post('/tags')
async def create_tag(tag: TagCreate) -> dict:
  return crud.create_tag(tag.name)

# create a tag on a post
@router.post('/posts/{post_id}/tags/{tag_id}')
async def add_tag(post_id: int, tag_id: int) -> dict:
  return crud.add_tag_to_post(post_id, tag_id)

# remove a tag from a post
@router.delete('/posts/{post_id}/tags/{tag_id}')
async def remove_tag(post_id: int, tag_id: int) -> dict:
  return crud.remove_tag_from_post(post_id, tag_id)

# create a report
@router.post('/reports')
async def create_report(report: ReportCreate) -> dict:
  return crud.create_report(report.post_id, report.reason)

# get reports
@router.get('/reports')
async def get_reports() -> list:
  return crud.get_reports()