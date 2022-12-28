from fastapi import Body, FastAPI, Request, logger , Form, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

import sys
import time

class Payload(BaseModel):
    R: str
    G: str
    B: str

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
async def rgb(
    background_tasks: BackgroundTasks,
    payload: Payload = Body(
        examples={
            "Red": {
                "summary" : "Red",
                "description": "Red",
                "value" : {
                    "R" : "255",
                    "G" : "0",
                    "B" : "0"
                }
            },
           "Blue": {
                "summary" : "Blue",
                "description": "Blue",
                 "value" : {
                    "R" : "0",
                    "G" : "0",
                    "B" : "255"
                }
            },
            "Green": {
                "summary" : "Green",
                "description": "Green",
                "value" : {
                    "R" : "0",
                    "G" : "255",
                    "B" : "0"
                }
            }
        })
    
    ):
    
    r= payload["R"]
    g= payload["G"]
    b= payload["B"]

    print(payload)
    background_tasks.add_task(write_rgb, r, g, b)
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

@app.get("/rgb/off")
async def rgb(background_tasks: BackgroundTasks):

    background_tasks.add_task(write_rgb, 0, 0 , 0)

    return {"message": "RGB set OFF"}