from ..database import conn
from .exception import handle_error
from fastapi import HTTPException

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