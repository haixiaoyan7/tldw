import os

def transcript_video(file_info str):
    """去 Server2 拉文件并保存到本地"""
    file_path = os.path.join(TEMP_DIR, f"{file_id}.srt")
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(f"{SERVER2_URL}/transcribe", json={"file_info": file_info}, timeout=120)
            resp.raise_for_status()
            with open(file_path, "wb") as f:
                f.write(resp.content)
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Request failed: {e}")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    return file_path

def analyze_video(file_info str):
    """去 Server3 拉文件并保存到本地"""
    file_path = os.path.join(TEMP_DIR, f"{file_id}.srt")
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(f"{SERVER3_URL}/analyze", json={"file_info": file_info}, timeout=120)
            resp.raise_for_status()
            with open(file_path, "wb") as f:
                f.write(resp.content)
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Request failed: {e}")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    return file_path

def get_srt(file_id: str):
    file_path = os.path.join(TEMP_DIR, f"{file_id}.srt")
    if os.path.exists(file_path):
        analyze_video(file_info)
    else:
        transcript_video(file_info)
        analyze_video(file_info)
        