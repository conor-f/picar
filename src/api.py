from car_manager import CarManager
import time

from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
from fastapi import Request


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
    return {"status": car_manager.stop()}


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
    car_manager.drive(l_speed=l_speed, r_speed=r_speed)
    return {"status": "driving", "direction": direction}


@app.post("/drive/{loops}")
async def drive_car(loops: int):
    try:
        for _ in range(loops):
            car_manager.drive(l_speed=0.4, r_speed=0.4)
            time.sleep(0.75)
            car_manager.stop()
            car_manager.drive(l_speed=0.4, r_speed=-0.4)
            time.sleep(0.75)
            car_manager.stop()

        return {"status": "success", "loops_completed": loops}
    except Exception as e:
        return {"status": "error", "message": str(e)}
