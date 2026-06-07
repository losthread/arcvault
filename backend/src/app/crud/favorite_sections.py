from ..db import conn
from .error_handler import handle_error
from fastapi import HTTPException

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