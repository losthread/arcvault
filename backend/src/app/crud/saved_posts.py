from ..db import conn
from .error_handler import handle_error
from fastapi import HTTPException

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
