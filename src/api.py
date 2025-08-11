from car_manager import CarManager
import asyncio

from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
from fastapi import Request
import cv2
from starlette.responses import StreamingResponse
import atexit


app = FastAPI()
car_manager = CarManager("192.168.178.61")
# Create a list of template directories to search
template_dirs = []
if os.path.exists("src/templates"):
    template_dirs.append("src/templates")
if os.path.exists("templates"):
    template_dirs.append("templates")

templates = Jinja2Templates(directory=template_dirs)


@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.post("/stop")
async def stop_car():
    await car_manager.stop()
    return {"status": "success"}


@app.post("/drive")
async def drive_direction(direction: str = Form(...)):
    """
    Drive the car in a single direction sent from the frontend.

    The HTMX buttons send the value in a form field named `direction`.
    Valid values: "up", "down", "left", "right".
    """
    print("asdf")
    mapping = {
        "up": (0.4, 0.4),
        "down": (-0.4, -0.4),
        "left": (0.4, -0.4),
        "right": (-0.4, 0.4),
    }

    if direction not in mapping:
        raise HTTPException(status_code=400, detail="Invalid direction")

    l_speed, r_speed = mapping[direction]
    await car_manager.drive(l_speed=l_speed, r_speed=r_speed)
    return {"status": "driving", "direction": direction}


@app.post("/drive/{loops}")
async def drive_car(loops: int):
    try:
        for _ in range(loops):
            await car_manager.drive(l_speed=0.4, r_speed=0.4)
            await asyncio.sleep(0.75)
            await car_manager.stop()
            await car_manager.drive(l_speed=0.4, r_speed=-0.4)
            await asyncio.sleep(0.75)
            await car_manager.stop()

        return {"status": "success", "loops_completed": loops}
    except Exception as e:
        return {"status": "error", "message": str(e)}


# ------------------------------------------------------------------------------
# Video streaming (MJPEG) endpoint
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Lazy webcam handling
# ------------------------------------------------------------------------------

# Will hold the cv2.VideoCapture instance once opened.  None until first /video
# request so that multiple Uvicorn workers do not all try to grab the camera.
video_capture: cv2.VideoCapture | None = None


def _get_camera() -> cv2.VideoCapture:
    """
    Open /dev/video0 the first time we need it and return the singleton handle.
    Subsequent calls just return the already-opened capture object.
    """
    global video_capture
    if video_capture is None:
        print("[video] Opening video device /dev/video0 ...")
        cap = cv2.VideoCapture("/dev/video0")
        if not cap.isOpened():
            raise RuntimeError("Could not open video device /dev/video0")
        print("[video] Video device opened successfully")
        video_capture = cap

        # Ensure the camera is released exactly once on process exit
        atexit.register(
            lambda: (print("[video] Releasing video device"), cap.release())
        )
    return video_capture


def _mjpeg_generator():
    """
    Continuously capture frames from the webcam and yield them as an MJPEG stream.
    """
    cap = _get_camera()
    while True:
        ok, frame = video_capture.read()
        if not ok:
            print("[video] Failed to read frame from camera")
            continue

        ok, jpg = cv2.imencode(".jpg", frame)
        if not ok:
            print("[video] Failed to encode frame as JPEG")
            continue

        frame_bytes = jpg.tobytes()
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n"
            b"Content-Length: "
            + f"{len(frame_bytes)}".encode()
            + b"\r\n\r\n"
            + frame_bytes
            + b"\r\n"
        )


@app.get("/video")
async def video_feed():
    """
    MJPEG video stream from the webcam.
    """
    print("[video] Client connected to /video stream")
    return StreamingResponse(
        _mjpeg_generator(),
        media_type="multipart/x-mixed-replace; boundary=frame",
    )


# camera release is registered when the camera is first opened in _get_camera()
