from .db import conn
from .schemas import SectionResponse, FolderResponse, PostResponse, PostCreate
from datetime import datetime

# return all the sections
def get_sections():
  # create a cursor to execute SQL
  cursor = conn.cursor()
  cursor.execute("SELECT section_id, name, description, slug, created_at FROM sections")

  # fetch query result as a list of tuples
  sections = cursor.fetchall()

  # convert list to SectionResponse pydantic object 
  response = list()
  for row in sections:
    section = SectionResponse(
      section_id = row[0],
      name = row[1],
      description = row[2],
      slug = row[3],
      created_at = row[4]
    )
    response.append(section)
  
  # close cursor
  cursor.close()

  # return json
  return response

# return all folders
def get_folders():
  # create a cursor to execute SQL
  cursor = conn.cursor()
  cursor.execute("SELECT folder_id, section_id, user_id, name, description, slug, created_at, updated_at FROM folders")


  # fetch query result as a list of tuples
  folders = cursor.fetchall()

  # convert list to FolderResponse pydantic object 
  response = list()
  for row in folders:
    folder = FolderResponse(
      folder_id=row[0],
      section_id=row[1],
      user_id=row[2],
      name=row[3],
      description=row[4],
      slug=row[5],
      created_at=row[6],
      updated_at=row[7]
    )
    response.append(folder)

  # close cursor
  cursor.close()

  # return json
  return response

# return all the posts
def get_posts():
  # create a cursor to execute SQL
  cursor = conn.cursor()
  cursor.execute("SELECT post_id, folder_id, user_id, title, content, created_at, updated_at FROM posts")

  # fetch query result as a list of tuples
  posts = cursor.fetchall()

  # convert list to FolderResponse pydantic object 
  response = list()
  for row in posts:
    post = PostResponse(
      post_id=row[0],
      folder_id=row[1],
      user_id=row[2],
      title=row[3],
      content=row[4],
      created_at=row[5],
      updated_at=row[6]
    )
    response.append(post)

  # close cursor
  cursor.close()

  return response

# create a post
def create_post(post):
  # create a cursor to execute SQL
  cursor = conn.cursor()

  # execute sql query (RETURNING immediately returns the inserted row instead of separate search)
  cursor.execute(
    """
      INSERT INTO posts(user_id, folder_id, title, content)
      VALUES (%s, %s, %s, %s)
      RETURNING post_id
    """,
    (1, post.folder_id, post.title, post.content)
  )
  # store returned tuple
  row = cursor.fetchone()
  post_id = row[0]

  # permanently save changes to DB and close
  conn.commit()
  cursor.close()

  return {"post_id": post_id}