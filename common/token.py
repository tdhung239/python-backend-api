from datetime import datetime, timedelta
from jose import JWTError, jwt
from schemas import login
from services.cookie_token import token
from fastapi import HTTPException, status
from config.settings import settings

# openssl rand -hex 32
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = int(settings.ACCESS_TOKEN_EXPIRE_MINUTES)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# def get_current_user():
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#
#     try:
#         data = token.values()[0]
#         payload = jwt.decode(data, SECRET_KEY, algorithms=[ALGORITHM])
#         email: str = payload.get("sub")
#
#         if email is None:
#             raise credentials_exception
#         token_data = login.TokenData(username=email)
#         return token_data.username
#
#     except JWTError:
#         raise credentials_exception
