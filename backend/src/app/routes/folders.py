from fastapi import APIRouter
from ..schemas import FolderCreate, FolderResponse
from ..crud import folders as f

router = APIRouter()

# get all folders
@router.get('/folders')
async def get_folders() -> list[FolderResponse]:
  return f.get_folders()

# create a folder
@router.post('/folders')
async def create_folder(folder: FolderCreate) -> dict:
  return f.create_folder(folder)

# update a folder
@router.put('/folders/{folder_id}')
async def update_folder(folder_id: int, folder: FolderCreate) -> dict:
  return f.update_folder(folder_id, folder)

# delete a folder
@router.delete('/folders/{folder_id}')
async def delete_folder(folder_id: int) -> dict:
  return f.delete_folder(folder_id)