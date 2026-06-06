from .db import conn
from .schemas import SectionResponse, FolderResponse, PostResponse, TagResponse, ReportCreate, ReportResponse
from datetime import datetime
from fastapi import HTTPException
from psycopg2.errors import UniqueViolation, ForeignKeyViolation

# error helper function
def handle_error(e, cursor):
  conn.rollback()
  cursor.close()

  # Data already exists (duplication)
  if isinstance(e, UniqueViolation):
    raise HTTPException(status_code=409, detail="Already exists")
  
  # Invalid reference error, data does not exist
  elif isinstance(e, ForeignKeyViolation):
    raise HTTPException(status_code=400, detail="Invalid reference")
  
  # Internal server
  else:
    raise HTTPException(status_code=500, detail="Internal server error")
  
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

  try:
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

  except Exception as e:
    handle_error(e, cursor)

# update a post
def update_post(post_id, post):
  # create a cursor to execute SQL
  cursor = conn.cursor()

  try:
    # execute sql query (RETURNING immediately returns the inserted row instead of separate search)
    cursor.execute(
      """
        UPDATE posts
        SET title = %s, content = %s, updated_at = NOW()
        WHERE post_id = %s AND user_id = %s
        RETURNING post_id
      """,
      (post.title, post.content, post_id, 1)
    )
    # store returned tuple
    row = cursor.fetchone()

    # http 404: resource does not exist
    if row is None:
      conn.rollback()
      cursor.close()
      raise HTTPException(status_code=404, detail=f"Post {post_id} does not exist")
    
    conn.commit()
    cursor.close()
    post_id = row[0]
    return {"post_id": post_id}
  
  # handle 404
  except Exception:
    raise
  
  except Exception as e:
    handle_error(e, cursor)

# delete a post
def delete_post(post_id):
  # create a cursor to execute sql
  cursor = conn.cursor()

  try:
    # execute sql query
    cursor.execute(
      """
        DELETE FROM posts
        WHERE post_id = %s AND user_id = %s
        RETURNING post_id
      """,
      (post_id, 1)
    )
    # store returned tuple
    row = cursor.fetchone()

    # http 404: resource does not exist
    if row is None:
      conn.rollback()
      cursor.close()
      raise HTTPException(status_code=404, detail=f"Post {post_id} does not exist")
    
    conn.commit()
    cursor.close()
    return {"deleted": True}
  
  # handle 404
  except Exception:
    raise
  
  except Exception as e:
    handle_error(e, cursor)

# create a folder
def create_folder(folder):
  # create a cursor to execute SQL
  cursor = conn.cursor()

  try:
    # execute sql query (RETURNING immediately returns the inserted row instead of separate search)
    cursor.execute(
      """
        INSERT INTO folders(user_id, section_id, name, description, slug)
        VALUES(%s, %s, %s, %s, %s)
        RETURNING folder_id
      """,
      (1, folder.section_id, folder.name, folder.description, folder.slug)
    )
    # store returned tuple
    row = cursor.fetchone()
    folder_id = row[0]
    # permanently save changes to DB and close
    conn.commit()
    cursor.close()
    return {"folder_id": folder_id}

  except Exception as e:
    handle_error(e, cursor)

# update a folder
def update_folder(folder_id, folder):
  cursor = conn.cursor()
  
  try:
    cursor.execute(
      """
        UPDATE folders
        SET name = %s, description = %s, slug = %s, updated_at = NOW()
        WHERE folder_id = %s AND user_id = %s
        RETURNING folder_id
      """,
      (folder.name, folder.description, folder.slug, folder_id, 1)
    )
    # store returned tuple
    row = cursor.fetchone()

    # http 404: resource does not exist
    if row is None:
      conn.rollback()
      cursor.close()
      raise HTTPException(status_code=404, detail=f"Folder {folder_id} does not exist")
    
    conn.commit()
    cursor.close()
    folder_id = row[0]
    return {"folder_id": folder_id}
  
  # handle 404
  except Exception:
    raise
  
  except Exception as e:
    handle_error(e, cursor)

# delete a folder
def delete_folder(folder_id):
  # create a cursor to execute sql
  cursor = conn.cursor()

  try:
    # execute sql query
    cursor.execute(
      """
        DELETE FROM folders
        WHERE folder_id = %s AND user_id = %s
        RETURNING folder_id
      """,
      (folder_id, 1)
    )
    # store returned tuple
    row = cursor.fetchone()

    if row is None:
      conn.rollback()
      cursor.close()
      raise HTTPException(status_code=404, detail=f"Folder {folder_id} not found")
    
    conn.commit()
    cursor.close()
    return {"deleted": True}
  
  # handle 404
  except Exception:
    raise
  
  except Exception as e:
    handle_error(e, cursor)

# create a personal note
def create_note(note):
  # create a cursor to execute SQL
  cursor = conn.cursor()

  try:
    # execute sql query (RETURNING immediately returns the inserted row instead of separate search)
    cursor.execute(
      """
        INSERT INTO notes(user_id, post_id, body)
        VALUES(%s, %s, %s)
        RETURNING note_id
      """,
      (1, note.post_id, note.body)
    )
    # store returned tuple
    row = cursor.fetchone()
    note_id = row[0]
    # permanently save changes to DB and close
    conn.commit()
    cursor.close()
    return {"note_id": note_id}

  except Exception as e:
    handle_error(e, cursor)

# update a personal note
def update_note(note_id, note):
  # create a cursor to execute SQL
  cursor = conn.cursor()

  try:
    # execute sql query (RETURNING immediately returns the inserted row instead of separate search)
    cursor.execute(
      """
        UPDATE notes
        SET body = %s, updated_at = NOW()
        WHERE note_id = %s AND user_id = %s
        RETURNING note_id 
      """,
      (note.body, note_id, 1)
    )
    # store returned tuple
    row = cursor.fetchone()

    # http 404: resource does not exist
    if row is None:
      conn.rollback()
      cursor.close()
      raise HTTPException(status_code=404, detail=f"Note {note_id} does not exist")
    
    conn.commit()
    cursor.close()
    note_id = row[0]
    return {"note_id": note_id}
  
  # handle 404
  except Exception:
    raise
  
  except Exception as e:
    handle_error(e, cursor)

# delete a personal note
def delete_note(note_id):
  # create a cursor to execute SQL
  cursor = conn.cursor()

  try:
    # execute sql query (RETURNING immediately returns the inserted row instead of separate search)
    cursor.execute(
      """
        DELETE FROM notes
        WHERE note_id = %s AND user_id = %s
        RETURNING note_id
      """,
      (note_id, 1)
    )
    # store returned tuple
    row = cursor.fetchone()

    if row is None:
      conn.rollback()
      cursor.close()
      raise HTTPException(status_code=404, detail=f"Note {note_id} not found")
    
    conn.commit()
    cursor.close()
    return {"deleted": True}

  # handle 404
  except Exception:
    raise  

  except Exception as e:
    handle_error(e, cursor)

# return a personal note
def get_notes(post_id):
  # create a cursor to execute SQL
  cursor = conn.cursor()

  # execute sql query (RETURNING immediately returns the inserted row instead of separate search)
  cursor.execute(
    """
      SELECT note_id, body, created_at 
      FROM notes
      WHERE post_id = %s AND user_id = %s
    """,
    (post_id, 1)
  )

  # fetch query result as a list of tuples
  notes = cursor.fetchall()

  # convert list to FolderResponse pydantic object 
  response = list()
  for row in notes:
    note = NoteResponse(
      note_id = row[0],
      body = row[1],
      created_at = row[2]
    )
    response.append(note)

  # close cursor
  cursor.close()
  
  return response

# upvote or downvote
def create_vote(vote):
  # create cursor
  cursor = conn.cursor()
  
  try:
    # execute sql
    cursor.execute(
      """
        INSERT INTO votes(post_id, user_id, is_upvote, created_at)
        VALUES(%s, %s, %s, NOW())
        RETURNING post_id
      """,
      (vote.post_id, 1, vote.is_upvote)
    )
    # store returned tuple
    row = cursor.fetchone()
    post_id = row[0]
    # permanently save changes to DB and close
    conn.commit()
    cursor.close()
    return {"post_id": post_id}

  except Exception as e:
    handle_error(e, cursor)

# update vote
def update_vote(post_id, vote):
  # create a cursor
  cursor = conn.cursor()

  try:  
    cursor.execute(
      """
        UPDATE votes
        SET is_upvote = %s
        WHERE post_id = %s AND user_id = %s
        RETURNING post_id
      """,
      (vote.is_upvote, post_id, 1)
    )
    # store returned tuple
    row = cursor.fetchone()

    # http 404: resource does not exist
    if row is None:
      conn.rollback()
      cursor.close()
      raise HTTPException(status_code=404, detail=f"Vote {post_id} does not exist")
    
    conn.commit()
    cursor.close()
    post_id = row[0]
    return {"post_id": post_id}
  
  # handle 404
  except Exception:
    raise
  
  except Exception as e:
    handle_error(e, cursor)

# return user's vote
def get_votes(post_id):
  # create a cursor
  cursor = conn.cursor()
  
  # execute SQL
  cursor.execute(
    """
      SELECT is_upvote
      FROM votes
      WHERE post_id = %s AND user_id = %s
    """,
    (post_id, 1)
  )
  # upvote
  row = cursor.fetchone()
  cursor.close()
  
  if row is None:
    return None
  
  vote_id = row[0]
  
  return {"is_upvote": vote_id}

# return net votes
def get_post_votes(post_id):
  cursor = conn.cursor()
  
  cursor.execute(
    """
      SELECT 
        COUNT(CASE WHEN is_upvote = true THEN 1 END) as upvotes,
        COUNT(CASE WHEN is_upvote = false THEN 1 END) as downvotes
      FROM votes
      WHERE post_id = %s
    """,
    (post_id,)
  )
  row = cursor.fetchone()
  upvotes = row[0]
  downvotes = row[1]

  cursor.close()
  
  return {
    "upvotes": upvotes,
    "downvotes": downvotes,
    "net": upvotes - downvotes
  }

# delete user's vote
def delete_vote(post_id):
  cursor = conn.cursor()
  
  try:
    cursor.execute(
      """
        DELETE FROM votes
        WHERE post_id = %s AND user_id = %s
        RETURNING post_id
      """,
      (post_id, 1)
    )
    # store returned tuple
    row = cursor.fetchone()

    # http 404: resource does not exist
    if row is None:
      conn.rollback()
      cursor.close()
      raise HTTPException(status_code=404, detail=f"Vote {post_id} does not exist")
    
    conn.commit()
    cursor.close()
    post_id = row[0]
    return {"deleted": True}
  
  # handle 404
  except Exception:
    raise
  
  except Exception as e:
    handle_error(e, cursor)

# save a post
def save_post(post_id):
  # create a cursor
  cursor = conn.cursor()

  try:
    # execute sql
    cursor.execute(
      """
        INSERT INTO saved_posts (post_id, user_id)
        VALUES (%s, %s)
        RETURNING post_id
      """,
      (post_id, 1)
    )
    row = cursor.fetchone() # fetch query results
    conn.commit() # commit changes to DB
    cursor.close() # close connections
    return {"post_id": row[0]}
  
  except Exception as e:
    handle_error(e, cursor)

# unsave a post
def unsave_post(post_id):
  # create a cursor
  cursor = conn.cursor()

  try:
    # execute sql
    cursor.execute(
      """
        DELETE FROM saved_posts
        WHERE post_id = %s AND user_id = %s
      """,
      (post_id, 1)
    )
    row = cursor.fetchone() # fetch query results
    # handle http: resource not found
    if row is None:
      conn.rollback() # undo changes to DB
      cursor.close()  # close connection
      raise HTTPException(status_code=404, detail="Not saved")
    
    # commit changes to DB
    conn.commit()
    cursor.close() # close connection
    return {"deleted": True}
  
  # raise 404
  except Exception:
    raise
  
  except Exception as e:
    handle_error(e, cursor)

# get saved posts
def get_saved_posts():
  # create cursor
  cursor = conn.cursor()

  cursor.execute("SELECT post_id FROM saved_posts WHERE user_id = %s", (1,))

  # fetch query results
  saved_posts = cursor.fetchall()
  cursor.close() # close connection

  response = list()
  for row in saved_posts:
    saved_post = {"post_id": row[0]}
    response.append(saved_post)
  
  return response

# mark a section favorite
def favorite_section(section_id):
  # create a cursor
  cursor = conn.cursor()

  try:
    # execute sql
    cursor.execute(
      """
        INSERT INTO favorite_sections (section_id, user_id)
        VALUES (%s, %s)
        RETURNING section_id
      """,
      (section_id, 1)
    )
    row = cursor.fetchone() # fetch query results
    conn.commit() # commit changes to DB
    cursor.close() # close connections
    return {"section_id": row[0]}
  
  except Exception as e:
    handle_error(e, cursor)

# unfavorite
def unfavorite_section(section_id):
  # create a cursor
  cursor = conn.cursor()

  try:
    # execute sql
    cursor.execute(
      """
        DELETE FROM favorite_sections 
        WHERE section_id = %s AND user_id = %s
        RETURNING section_id
      """,
      (section_id, 1)
    )
    row = cursor.fetchone() # fetch query results
    
    if row is None:
      conn.rollback()
      cursor.close()
      raise HTTPException(status_code=404, detail="Not favorite")
    
    conn.commit()
    cursor.close()
    return {"deleted": True}
  
  # raise 404
  except Exception:
    raise
  
  except Exception as e:
    handle_error(e, cursor)

# get all the favorite sections
def get_favorite_sections():
  # create cursor
  cursor = conn.cursor()

  cursor.execute("SELECT section_id FROM favorite_sections WHERE user_id = %s", (1,))

  # fetch query results
  favorite_sections = cursor.fetchall()
  cursor.close() # close connection

  response = list()
  for row in favorite_sections:
    favorite_section = {"section_id": row[0]}
    response.append(favorite_section)
  
  return response

# create a tag
def create_tag(tag_name):
  cursor = conn.cursor()
  try:
    cursor.execute(
      "INSERT INTO tags(name) VALUES(%s) RETURNING tag_id",
      (tag_name,)
    )
    row = cursor.fetchone()
    conn.commit()
    cursor.close()
    return {"tag_id": row[0]}
  except Exception as e:
    handle_error(e, cursor)

# get all tags
def get_tags():
  cursor = conn.cursor()
  cursor.execute("SELECT tag_id, name FROM tags")
  tags = cursor.fetchall()
  cursor.close()
  
  response = list()
  for row in tags:
    tag = TagResponse(tag_id=row[0], name=row[1])
    response.append(tag)
  
  return response

# get tags for a post
def get_post_tags(post_id):
  cursor = conn.cursor()
  cursor.execute(
    """
      SELECT tags.tag_id, tags.name 
      FROM tags
      JOIN post_tags ON tags.tag_id = post_tags.tag_id
      WHERE post_tags.post_id = %s
    """,
    (post_id,)
  )
  tags = cursor.fetchall()
  cursor.close()
  
  response = list()
  for row in tags:
    tag = TagResponse(tag_id=row[0], name=row[1])
    response.append(tag)
  
  return response

# Add tag to post
def add_tag_to_post(post_id, tag_id):
  cursor = conn.cursor()
  try:
    cursor.execute(
      """
        INSERT INTO post_tags(post_id, tag_id) VALUES(%s, %s) 
        RETURNING post_id""",
      (post_id, tag_id)
    )
    row = cursor.fetchone()
    conn.commit()
    cursor.close()
    return {"post_id": row[0]}
  
  except Exception as e:
    handle_error(e, cursor)

# Remove tag from post
def remove_tag_from_post(post_id, tag_id):
  cursor = conn.cursor()
  try:
    cursor.execute(
      """
        DELETE FROM post_tags 
        WHERE post_id = %s AND tag_id = %s RETURNING post_id
      """,
      (post_id, tag_id)
    )
    row = cursor.fetchone()
    
    if row is None:
      cursor.close()
      raise HTTPException(status_code=404, detail="Tag not on post")
    
    conn.commit()
    cursor.close()
    return {"deleted": True}
  
  # raise 404
  except Exception:
    raise

  except Exception as e:
    handle_error(e, cursor)

# create report
def create_report(post_id, reason):
  cursor = conn.cursor()
  try:
    cursor.execute(
      """
        INSERT INTO reports(post_id, user_id, reason, created_at)
        VALUES(%s, %s, %s, NOW())
        RETURNING report_id
      """,
      (post_id, 1, reason)
    )
    row = cursor.fetchone()
    conn.commit()
    cursor.close()
    return {"report_id": row[0]}
  
  except Exception as e:
    handle_error(e, cursor)

# get reports
def get_reports():
  cursor = conn.cursor()
  cursor.execute(
    """
      SELECT report_id, post_id, reason, created_at 
      FROM reports 
      WHERE user_id = %s
    """, 
    (1,)
  )
  reports = cursor.fetchall()
  cursor.close()
  
  response = list()
  for row in reports:
    report = ReportResponse(report_id=row[0],post_id=row[1], reason=row[2], created_at=row[3])

    response.append(report)
  
  return response