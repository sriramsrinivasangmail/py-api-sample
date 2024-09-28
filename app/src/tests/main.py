#! /usr/bin/env python

import json
import logging
import os
import jinja2

from fastapi import (
    FastAPI,
    Header,
    HTTPException,
    Request,
    Response,
)

app = FastAPI()

# Health check endpoint
@app.get("/healthz")
async def healthz():
    return "OK"


@app.get("/readyz")
def readyz():
    ap = os.getenv("HOME")
    if ap is None:
        raise HTTPException(status_code=500, detail="HOME is not set")
    return "OK"

# Run the application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=20080
    )
