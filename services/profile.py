import shutil
from fastapi import UploadFile, File
from sqlalchemy.orm import Session
from models.user import User
from models.role import Role
from models.profile import Profile
from schemas.profile import ProfileSchemaUpdateImage
from utils.profile import update_image_profie


class ProfileService:

    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def get_profile(self, current_user):

        try:
            result = self.db_session.query(Profile).join(User).join(Role).filter(User.email == current_user)
            rs = [{
                "id": item.id,
                "role_name": item.users_profiles.roles.role_name,
                "first_name": item.first_name,
                "last_name": item.last_name,
                "avatar": item.avatar,
                "email": item.users_profiles.email,
                "user_name": item.users_profiles.user_name,
                "gender": item.gender,
                "date_of_birth": item.date_of_birth,
                "phone": item.phone,
                "address": item.address
            } for item in result]
            return rs

        except Exception as ex:
            raise ex

    async def update_image_profile(self, current_user, data: ProfileSchemaUpdateImage):

        try:
            update_pf = self.db_session.query(Profile).filter(User.email == current_user).first()

            if not update_pf:
                raise ValueError(f"Profile with id not existed")

            update_pf.avatar = data.avatar
            self.db_session.add(update_pf)
            self.db_session.flush()
            return "successfully"

        except Exception as ex:
            raise ex

    async def update_image_profile2(self, current_user, file: UploadFile = File(...)):

        try:
            update_pf = self.db_session.query(Profile).filter(User.email == current_user).first()

            if not update_pf:
                raise ValueError(f"Profile with id not existed")

            with open(f'{file.filename}', 'wb') as buffer:
                shutil.copyfileobj(file.file, buffer)
            update_image_profie(self, update_pf, file)
            return "successfully"

        except Exception as ex:
            raise ex
