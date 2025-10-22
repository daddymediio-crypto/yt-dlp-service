from fastapi import FastAPI, HTTPException, Query
from yt_dlp import YoutubeDL

app = FastAPI()

@app.get("/fetch-video")
def fetch_video(url: str = Query(..., description="YouTube video URL")):
    if "youtube.com" not in url and "youtu.be" not in url:
        raise HTTPException(status_code=400, detail="Invalid YouTube URL")
    
    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "quiet": True,
        "skip_download": True
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
        
        formats = []
        for f in info.get("formats", []):
            if f.get("url"):
                formats.append({
                    "format_id": f.get("format_id"),
                    "ext": f.get("ext"),
                    "quality": f.get("format_note") or f.get("height") or "audio",
                    "url": f.get("url")
                })

        return {
            "title": info.get("title"),
            "thumbnail": info.get("thumbnail"),
            "duration": info.get("duration"),
            "uploader": info.get("uploader"),
            "formats": formats
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
