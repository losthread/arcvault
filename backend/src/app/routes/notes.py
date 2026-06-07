from fastapi import APIRouter
from ..schemas import NoteCreate, NoteUpdate, NoteResponse
from ..crud import notes as n

router = APIRouter()

# create a private note
@router.post('/notes')
async def create_note(note: NoteCreate) -> dict:
  return n.create_note(note)

# update a private note
@router.put('/notes/{note_id}')
async def update_note(note_id: int, note: NoteUpdate) -> dict:
  return n.update_note(note_id, note)

# delete a private note
@router.delete('/notes/{note_id}')
async def delete_note(note_id: int) -> dict:
  return n.delete_note(note_id)

# get a private note
@router.get('/notes/{post_id}')
async def get_notes(post_id: int) -> list[NoteResponse]:
  return n.get_notes(post_id)