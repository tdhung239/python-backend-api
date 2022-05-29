from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse
from controller.role import router as role_router
from controller.category import router as category_router
from controller.user import router as user_router
from controller.profile import router as profile_router
from controller.post import router as post_router
from controller.logpost import router as logpost_router
from controller.likepost import router as likepost_router
from controller.confession import router as confession_router
from controller.potscomment import router as potscomment_router
from controller.banner import router as banner_router
from controller.bannershow import router as bannershow_router
from controller.login import router as login_router

api_router = APIRouter(default_response_class=ORJSONResponse)
api_router.include_router(login_router)
api_router.include_router(bannershow_router)
api_router.include_router(banner_router)
api_router.include_router(potscomment_router)
api_router.include_router(confession_router)
api_router.include_router(likepost_router)
api_router.include_router(logpost_router)
api_router.include_router(post_router)
api_router.include_router(role_router)
api_router.include_router(category_router)
api_router.include_router(user_router)
api_router.include_router(profile_router)
