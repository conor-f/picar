# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "fastapi",
#   "pydantic",
#   "requests",
#   "uvicorn",
# ]
# ///
from api import app
import uvicorn

uvicorn.run(app, host="127.0.0.1", port=8000)
