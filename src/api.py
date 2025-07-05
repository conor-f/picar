from car_manager import CarManager
import time

from fastapi import FastAPI


app = FastAPI()
car_manager = CarManager("192.168.178.61")


@app.post("/stop")
async def stop_car():
    return {"status": car_manager.stop()}


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
