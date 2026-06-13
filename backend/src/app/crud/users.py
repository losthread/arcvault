from ..config import conn
from ..auth import hash_password, verify_password, create_jwt_token
from ..crud.exception import handle_error
from fastapi import HTTPException

# create the user and put the hashed password
def register(username, email, password):
  cursor = conn.cursor()
  
  try:
    # hash the pass
    hashed_password = hash_password(password)

    cursor.execute(
      """
        INSERT INTO users(username, email, password_hash, profile_picture_url, bio, created_at)
        VALUES (%s, %s, %s, %s, %s, NOW())
        RETURNING user_id
      """,
      (username, email, hashed_password, None, None)
    )
    # fetch query results
    row = cursor.fetchone()
    # commit changes to DB
    conn.commit()
    cursor.close()

    return {"user_id": row[0]}

  # handle database errors
  except Exception as e:

    handle_error(e, cursor)

# login user
def login(email, password):
  cursor = conn.cursor()

  try:
    cursor.execute(
      """
        SELECT user_id, password_hash 
        FROM users
        WHERE email = %s
      """,
      (email,)
    )
    row = cursor.fetchone()

    # http 401: if user is not found
    if row is None:
      cursor.close()
      raise HTTPException(status_code=401, detail="Account doesn't exist")
    
    user_id = row[0]
    stored_password_hash = row[1]

    # verify password
    if not verify_password(password, stored_password_hash):  # password first:
      cursor.close()
      raise HTTPException(status_code=401, detail="Email or password is incorrect")
    
    # create token
    token = create_jwt_token(user_id)
    cursor.close()

    return {
      "access_token": token,
      "token_type": "bearer",
      "user_id": user_id
    }
  
  # handle http 404
  except HTTPException:
    raise

  # handle DB errors
  except HTTPException as e:
    handle_error(e, cursor)

# get your info
def get_current_user_details(user_id):
  cursor = conn.cursor()

  try:
    cursor.execute(
      """
        SELECT user_id, username, email, profile_picture_url, bio, created_at
        FROM users
        WHERE user_id = %s
      """,
      (user_id,)
    )
    row = cursor.fetchone()

    if row is None:
      cursor.close()
      raise HTTPException(status_code=404, detail="User not found")
    
    cursor.close()

    return {
      "user_id": row[0],
      "username": row[1],
      "email": row[2],
      "profile_picture_url": row[3],
      "bio": row[4],
      "created_at": row[5]
    }
  
  # catch 404 not found
  except HTTPException:
    raise

  # handle DB errors
  except Exception as e:
    cursor.close()
    handle_error(e, cursor)

# other user's details
def get_user_details(user_id: int):
  # create cursor
  cursor = conn.cursor()
  
  try:
    cursor.execute(
      """
        SELECT user_id, username, profile_picture_url, bio, created_at
        FROM users
        WHERE user_id = %s
      """,
      (user_id,)
    )
    row = cursor.fetchone()
  
    # if user not found
    if row is None:
      cursor.close()
      raise HTTPException(status_code=404, detail="User not found")

    cursor.close()
    
    return {
      "user_id": row[0],
      "username": row[1],
      "profile_picture_url": row[2],
      "bio": row[3],
      "created_at": row[4]
    }
  
  # catch 404 not found
  except HTTPException:
    raise

  # handle DB errors
  except Exception as e:
    handle_error(e, cursor)