from .config import conn
from argon2 import PasswordHasher
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from argon2.exceptions import VerificationError, VerifyMismatchError, InvalidHashError
import jwt
import os

load_dotenv()

JWT_SECRET = os.getenv("JWT_KEY")
ALGORITHM = "HS256"

# instantiate password hashing object
ph = PasswordHasher()

# hash given password when registering
def hash_password(password: str) -> str:
  hashed_password = ph.hash(password)
  return hashed_password

# verify login password with stored hash in DB
def verify_password(password: str, stored_hash: str) -> bool:
  try:
    ph.verify(stored_hash, password)
    return True

  except (VerifyMismatchError, VerificationError, InvalidHashError):
    return False

# create JWT token and send to user
def create_jwt_token(user_id: int) -> str:

  payload = {
    "user_id": user_id,
  }

  # encode the payload to create final token string
  token = jwt.encode(payload, JWT_SECRET, algorithm=ALGORITHM)
  return token

# extract user_id from JWT received token
def decode_jwt_token(token: str):
  try:
    payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
    user_id = payload["user_id"]

    return user_id
  
  except Exception as e:
    print("JWT DECODING FAILED")
    print(repr(e))
    return None