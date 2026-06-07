from ..db import conn
from psycopg2.errors import UniqueViolation, ForeignKeyViolation
from fastapi import HTTPException

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