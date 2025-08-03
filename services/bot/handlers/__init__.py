from .common import router as common_router
from .register import router as register_router
from .login import router as login_router
from .lead import router as lead_router


all_routers = [common_router, register_router, login_router, lead_router]