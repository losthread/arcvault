from ..database import conn
from ..schemas import NoteResponse
from .exception import handle_error
from fastapi import HTTPException

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
