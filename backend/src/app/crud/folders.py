from ..db import conn
from ..schemas import FolderResponse
from .error_handler import handle_error
from fastapi import HTTPException

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