from ..db import conn
from ..schemas import TagResponse
from .error_handler import handle_error
from fastapi import HTTPException

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