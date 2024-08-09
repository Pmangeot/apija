from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from fastapi.staticfiles import StaticFiles # type: ignore
from os.path import dirname, abspath, join
from fastapi.openapi.utils import get_openapi
from fastapi.openapi.docs import get_swagger_ui_html

import sys
sys.path.append('/api/root')

from api.root import api_router
from core.config import settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connection des fichiers au repertoire "/documents"
#app.mount("/documents", StaticFiles(directory=join(abspath(dirname(__file__)), "documents")), name="documents")

# Connection au router de l'API
app.include_router(api_router, prefix=settings.API_STR)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=80, log_level="debug", reload=True, reload_dirs=["./app"])