from fastapi import Body, FastAPI

import sys
import time

import motephat


motephat.set_brightness(1)
motephat.set_clear_on_exit(True)

def usage():
    print("Usage: {} <r> <g> <b>".format(sys.argv[0]))
    sys.exit(1)


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "mote-phat-api"}


@app.post("/rgb")
async def rgb(payload: dict = Body(...)):
    print(payload)

    # Exit if non integer value. int() will raise a ValueError
    try:
        r=int(payload['R'])
        g=int(payload['G'])
        b=int(payload['B'])
    except ValueError:
        return {"message": "RGB should be Integager value" }

    # Exit if any of r, g, b are greater than 255
    if max(r, g, b) > 255:
        return {"message": "RGB should be Integager value between 0-255" }


    while True:

        for channel in range(4):
            for pixel in range(16):
                motephat.set_pixel(channel + 1, pixel, r, g, b)
            time.sleep(0.01)

    motephat.show()

    # return {"message": "RGB set R:" + {payload['R']} }
    return {"message": "RGB set RGB"}