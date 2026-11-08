from __future__ import annotations

from typing import Any

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    a: int | float
    b: int | float
    op: str


class CalcResponse(BaseModel):
    result: int | float


@app.post("/")
def calc(item: Item):
    a = item.a
    b = item.b
    op = item.op
    result: Any = None

    match op:
        case "add":
            result = a + b
        case "sub":
            result = a - b
        case "mul":
            result = a * b
        case "div":
            if b == 0:
                raise HTTPException(
                    status.HTTP_400_BAD_REQUEST,
                    detail="Division by zero",
                )
            result = a / b
        case _:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported operator: {op}",
            )

    return CalcResponse(result=result)
