from http import HTTPStatus
from typing import Optional
from fastapi import HTTPException

def make_bad_request_response(ex):
    result_bad = {
        "code": HTTPStatus.BAD_REQUEST,
    }
    result_bad.update({"result": str(ex)})
    raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=result_bad)


def make_oke_request_response(item_dict: Optional[dict] = None):
    result_oke = {
        "code": HTTPStatus.OK
    }

    if item_dict is None:
        return result_oke
    result_oke.update(item_dict)
    return result_oke
