from .start import router as start_router
from .register import router as register_router
from .login import router as login_router


all_routers = [start_router, register_router, login_router]