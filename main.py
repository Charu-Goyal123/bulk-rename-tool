from fastapi import FastAPI, HTTPException, Query
from scraper import scrape_reels
from modals import Reel
from typing import List

app = FastAPI()

@app.get("/scrape", response_model=List[Reel])
async def scrape(username: str = Query(..., min_length=1), limit: int = Query(20, ge=1, le=100)):
    try:
        reels = await scrape_reels(username, limit)
        if not reels:
            raise HTTPException(status_code=404, detail="No public reels found or user not found.")
        return reels
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal error while scraping.")