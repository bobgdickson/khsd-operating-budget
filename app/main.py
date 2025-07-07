from fastapi import FastAPI

from app.database import engine, Base
from app.routers import budgets

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Operating Budget API")

app.include_router(budgets.router)

try:
    from fastapi.templating import Jinja2Templates
    from app.routers import ui

    templates = Jinja2Templates(directory="app/templates")
    app.include_router(ui.router)
except ImportError:
    # Templating dependencies not available; skip UI
    pass