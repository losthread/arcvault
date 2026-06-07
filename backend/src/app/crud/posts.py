from ..db import conn
from ..schemas import PostResponse
from .error_handler import handle_error
from fastapi import HTTPException

# return all the posts
def get_posts():
  # create a cursor to execute SQL
  cursor = conn.cursor()
  cursor.execute(
    """
      SELECT post_id, folder_id, user_id, title, content, created_at, updated_at 
      FROM posts
    """
  )

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
