from function import Prediction
from function import Model
from function import interval
from fastapi import FastAPI

app = FastAPI()

knc = Model()

@app.get("/items")
async def input_predictions(T: int, H: int, P: int, V: int, ST: int):
    try:
        T = interval(T, -150, 150)
        H = interval(H, 0, 100)
        P = interval(P, 0, 100)
        V = interval(V, 0, 100)
        ST = interval(ST, 0, 23)
        result = Prediction(knc, T, H, P, V, ST)
        return {"severity": str(result)}
    except ValueError:
        return "data entry error"