from function import prediction
from function import model
from function import interval
from fastapi import FastAPI

app = FastAPI()

dtc = model()

@app.get("/items")
async def input_predictions(t: int, h: int, p: int, v: int, st: int):
    try:
        t = interval(t, -150, 150)
        h = interval(h, 0, 100)
        p = interval(p, 0, 100)
        v = interval(v, 0, 100)
        st = interval(st, 0, 23)
        result = prediction(dtc, t, h, p, v, st)
        return {"severity": str(result)}
    except ValueError:
        return "data entry error"