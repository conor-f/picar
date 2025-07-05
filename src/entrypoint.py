# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "fastapi",
#   "pydantic",
#   "requests",
#   "uvicorn",
#   "jinja2",
#   "python-multipart",
# ]
# ///
from api import app
import uvicorn

uvicorn.run(app, host="127.0.0.1", port=8000)
