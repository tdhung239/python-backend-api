import json
import re
import smtplib
import ssl

from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPBasicCredentials
from starlette.status import HTTP_401_UNAUTHORIZED

from config.database import get_db_session
from models.user import User

security = HTTPBearer()


async def verify(credentials: HTTPBasicCredentials = Depends(security)):
    access_token = credentials.credentials
    db_session = next(get_db_session())
    try:
        user = db_session.execute(f"SELECT * FROM tbl_user WHERE token = '{access_token}'").fetchone()
        if not user:
            raise HTTPException(
                detail="Invalid Authorization token",
                status_code=HTTP_401_UNAUTHORIZED,
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user.email
    except Exception as ex:
        raise ex


def send_mail(password_genarate: str, port: int, smtp_server: str, sender_email: str, password: str,
              receiver_email: str):
    message = """\
                            Subject: System Hybrid provide pass login for you

                            new pass generate of you is """ + password_genarate

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)


def validate_email(email: str):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if (re.fullmatch(regex, email)):
        return True
    else:
        return False
