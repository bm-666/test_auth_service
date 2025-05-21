from .auth.endpoints import auth_routers
from .user.endpoints import user_router

# Список роутеров
routers = [auth_routers, user_router]
