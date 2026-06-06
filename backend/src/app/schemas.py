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

class TagCreate(BaseModel):
  name: str

# Votes
class VoteCreate(BaseModel):
  post_id: int
  is_upvote: bool # true for upvote and false for downvote

# Notes
class NoteCreate(BaseModel):
  post_id: int
  body: str

class NoteUpdate(BaseModel):
  body: str

class NoteResponse(BaseModel):
  note_id: int
  body: str
  created_at: datetime

# reports
class ReportCreate(BaseModel):
  post_id: int
  reason: str

class ReportResponse(BaseModel):
  report_id: int
  post_id: int
  reason: str
  created_at: datetime