import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from pipeline import run_pipeline_stream, run_pipeline

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    prompt: str

@app.post("/generate")
def generate(req: PromptRequest):
    result = run_pipeline(req.prompt)
    return result.model_dump()

@app.post("/generate/stream")
def generate_stream(req: PromptRequest):
    def event_stream():
        for stage, result in run_pipeline_stream(req.prompt):
            if stage == "__retry__":
                # result is {"stage": ..., "attempt": ...}
                payload = json.dumps({
                    "stage": result["stage"],
                    "done": False,
                    "retrying": True,
                    "attempt": result["attempt"],
                })
                yield f"data: {payload}\n\n"
            elif result is None:
                payload = json.dumps({"stage": stage, "done": False})
                yield f"data: {payload}\n\n"
            else:
                payload = json.dumps({
                    "stage": stage,
                    "done": True,
                    "data": result.model_dump(),
                })
                yield f"data: {payload}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")