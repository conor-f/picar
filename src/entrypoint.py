# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "fastapi",
#   "pydantic",
#   "httpx",
#   "uvicorn",
#   "jinja2",
#   "python-multipart",
#   "opencv-python-headless",
# ]
# ///
from api import app
import uvicorn

uvicorn.run(app, host="0.0.0.0", port=8000)
