#  uvicorn main:app --host 0.0.0.0 --port 8001 --reload

import asyncio
from fastapi import FastAPI
import uvicorn

from consumers.metric_consumer import consume_metric_events

app = FastAPI(title="Metric Consumer Microservice")

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(consume_metric_events())

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
