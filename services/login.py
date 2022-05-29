from sqlalchemy.orm import Session
from models.user import User
from services.cookie_token import token
from schemas.login import LoginSchema, EmailSchema
from common.token import create_access_token
from common.auth import send_mail
from config.settings import settings
import secrets
import string
import bcrypt


class LoginService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def login(self, data: LoginSchema):

        try:
            user = self.db_session.execute(f"SELECT * FROM tbl_user WHERE email = '{data.email}'").fetchone()

            if user:
                matched = bcrypt.checkpw(data.password.encode('utf-8'), user.password.encode('utf-8'))
                if not matched:
                    raise ValueError(f"Error enter email or pass not successfully")
                else:
                    access_token = create_access_token({"sub": user.email})
                    self.db_session.execute(f"UPDATE tbl_user SET token='{access_token}' WHERE id={user.id}")
                    self.db_session.flush()
                    return {"result": "successfully", "token": access_token}
            else:
                raise ValueError(f"Error enter email or pass not successfully")

        except Exception as ex:
            raise ex

    async def logout(self, email):

        try:
            self.db_session.execute(f"UPDATE tbl_user SET token='' WHERE email='{email}'")
            self.db_session.flush()
            return {"result": "successfully"}
        except Exception as ex:
            raise ex

    async def forgot_password(self, data: EmailSchema):
        port = settings.PORT
        smtp_server = settings.SMTP_SERVER
        sender_email = settings.SENDER_EMAIL
        receiver_email = data.email
        password = settings.PASSWORD

        try:
            count_user = self.db_session.query(User.email).filter(User.email == data.email).count()

            if count_user:
                alphabet = string.ascii_letters + string.digits
                password_genarate = ''.join(secrets.choice(alphabet) for i in range(20))
                self.update_genrenate_pass(password_genarate, data)
                send_mail(password_genarate, port, smtp_server, sender_email, password, receiver_email)
                return {"result": "successfully"}
            else:
                raise ValueError(f"Error enter email not successfully")

        except Exception as ex:
            raise ex

    def dict_user_pass(sefl, User, email):
        user_pass = sefl.db_session.query(User.email, User.password, User.token).filter(
            User.email == email)
        dict_user_pass = list(map(lambda item: dict(item), user_pass))[0]
        return dict_user_pass

    def update_genrenate_pass(self, password_genarate: str, data):
        update_pf = self.db_session.query(User).filter(User.email == data.email).first()

        if not update_pf:
            raise ValueError(f"Profile with id not existed")
        hashed_pass_in = self.hashed_pass(password_genarate)
        update_pf.password = hashed_pass_in
        self.db_session.add(update_pf)
        self.db_session.flush()

    def hashed_pass(self, data_in: str):
        data_in = data_in.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(data_in, salt)
        str_hash = str(hashed)
        str_hash = str_hash[str_hash.find("'") + 1:str_hash.rfind("'")]
        return str_hash
