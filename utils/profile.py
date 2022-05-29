from fastapi import UploadFile, File


def update_image_profie(self, update_pf: dict, file: UploadFile = File(...)):
    if file.filename is not None:
        update_pf.avatar = file.filename
    self.db_session.add(update_pf)
    self.db_session.flush()
