from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from getVedio import get_file_info
from transcript import transcribe
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UrlRequest(BaseModel):
    url: str

TEMP_DIR = "/tmp/tldw"

@app.post("/api/analyze")
async def process_url(request: UrlRequest):
    file_info = get_file_info(request.url)
    if not file_info:
        async def fail_stream():
            yield "data: ERROR: can't get file\n\n"
        return StreamingResponse(fail_stream(), media_type="text/event-stream")
    file_path = os.path.join(TEMP_DIR, f"{file_id}.srt")

    async def gen():
        yield "data: get video...\n\n"
        file_info = get_file_info(request.url)
        download_url = file_info.get("download_url")
        # transcribe(download_url)

        yield "data: analyze video...\n\n"
        # transcription_result = await transcribe_video()
        # yield f"data: {transcription_result}\n\n"

        yield "data: generate summary...\n\n"
        # summary_result = await summarize()
        # yield f"data: {summary_result}\n\n"

        # 完成
        yield "data: Done\n\n"

    return StreamingResponse(gen(), media_type="text/event-stream")

