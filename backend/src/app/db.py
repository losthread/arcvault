# Pydantic models for validation
from pydantic import BaseModel #, EmailStr
from datetime import datetime

# Sections
class SectionResponse(BaseModel):
  section_id: int
  name: str
  description: str | None = None
  slug: str
  created_at: datetime

# Folders
class FolderCreate(BaseModel):
  section_id: int
  name: str
  description: str | None = None
  slug: str

class FolderResponse(BaseModel):
  folder_id: int
  section_id: int
  user_id: int
  name: str
  description: str | None = None
  slug: str
  created_at: datetime
  updated_at: datetime

# Posts
class PostCreate(BaseModel):
  folder_id: int
  title: str
  content: str

class PostUpdate(BaseModel):
  title: str | None = None
  content: str | None = None

class PostResponse(BaseModel):
  post_id: int
  folder_id: int
  user_id: int
  title: str
  content: str
  created_at: datetime
  updated_at: datetime

# Tags
class TagResponse(BaseModel):
  tag_id: int
  name: str

# # Auth
# class UserRegister(BaseModel):
#   username: str
#   email: str
#   password: str

# class UserLogin(BaseModel):
#   email: EmailStr
#   password: str

# class UserResponse(BaseModel):
#   user_id: int
#   username: str
#   email: str
#   profile_picture_url: str | None = None
#   bio: str | None = None
#   created_at: datetime