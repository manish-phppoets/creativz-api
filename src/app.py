from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.routes.customers   import router as customerRoutes
from src.routes.website.settings   import router as settingRoutes
from src.authentication import router as authRoutes

from src.configuration.database import databaseStartup,databaseShutdown

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.add_event_handler("startup", databaseStartup)
app.add_event_handler("shutdown",databaseShutdown)


app.include_router(authRoutes,prefix='/api/auth',  tags=['authentication'])
app.include_router(customerRoutes,prefix='/api/customers', tags=['customers'])
app.include_router(settingRoutes,prefix='/website/settings', tags=['settings'])

