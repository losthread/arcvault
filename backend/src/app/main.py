from fastapi import FastAPI
from .routes import contribution, favorite_sections, folders, notes, posts, reports, saved_posts, sections, tags, votes, users
import uvicorn

# fastAPI app instance - contains: settings, middleware, endpoints
# app that uvicorn serves
app = FastAPI()

# Include the router instance from routes.py into app
app.include_router(contribution.router)
app.include_router(favorite_sections.router)
app.include_router(folders.router)
app.include_router(notes.router)
app.include_router(posts.router)
app.include_router(reports.router)
app.include_router(saved_posts.router)
app.include_router(sections.router)
app.include_router(tags.router)
app.include_router(votes.router)
app.include_router(users.router)

# Run the dev ASGI server on localhost when main.py is run
if __name__ == "__main__":
  print(f"Welcome to arcvault version 1.0.0")
  uvicorn.run("src.app.main:app", host = "0.0.0.0", port = 8000, reload = True)