from __future__ import annotations

from typing import Any

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel


class CalcResponse(BaseModel):
    result: int | float


app = FastAPI()


@app.get("/{a}/{op}/{b}")
def calc(a: int, op: str, b: int) -> CalcResponse:
    result: Any = None
    if not str in ["add", "sub", "mul", "div"]:
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
