from fastapi import Body, FastAPI, Request, logger , Form, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

import sys
import time


class Data(BaseModel):
    field: str


import motephat


motephat.set_brightness(1)
motephat.set_clear_on_exit(True)

app = FastAPI()

def write_rgb(red: int, green: int , blue: int):
    print(red, green, blue )
    # while True:
    for channel in range(4):
        for pixel in range(16):
            motephat.set_pixel(channel + 1, pixel, red, green , blue )
        time.sleep(0.01)

    motephat.show()


app.mount("/static", StaticFiles(directory="static"), name="static")

# templates = Jinja2Templates(directory="templates")

@app.get("/")
async def root(request: Request):
    # return templates.TemplateResponse("rgb.html", {"request": request})
    return {"message": "ROOT"}




@app.post("/rgb")
async def rgb(payload: Request = Body(...)):
    # logger.debug(Data)
    
    print(payload)
    # print(payload['R'])
    # Exit if non integer value. int() will raise a ValueError
    # try:
    #     r=int(payload['R'])
    #     g=int(payload['G'])
    #     b=int(payload['B'])
    # except ValueError:
    #     return {"message": "RGB should be Integager value" }

    # Exit if any of r, g, b are greater than 255
    # if max(r, g, b) > 255:
    #     return {"message": "RGB should be Integager value between 0-255" }


    # while True:

    #     for channel in range(4):
    #         for pixel in range(16):
    #             motephat.set_pixel(channel + 1, pixel, r, g, b)
    #         time.sleep(0.01)

    # motephat.show()

    # return {"message": "RGB set R:" + {payload['R']} }
    return {"message": "RGB set RGB"}



@app.get("/rgb/red")
async def rgb(background_tasks: BackgroundTasks):

    background_tasks.add_task(write_rgb, 255, 0, 0)
    return {"message": "RGB set Red"}
    
@app.get("/rgb/green")
async def rgb(background_tasks: BackgroundTasks):

    background_tasks.add_task(write_rgb, 0, 255 ,0 )

    return {"message": "RGB set Green"}

@app.get("/rgb/blue")
async def rgb(background_tasks: BackgroundTasks):

    background_tasks.add_task(write_rgb, 0, 0 , 255)

    return {"message": "RGB set Blue"}