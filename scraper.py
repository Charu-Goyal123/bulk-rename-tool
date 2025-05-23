from playwright.async_api import async_playwright
from modals import Reel
import re

async def scrape_reels(username: str, limit: int = 20):
    url = f"https://www.instagram.com/{username}/reels/"
    reels = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto(url, timeout=60000)

        # Scroll to load more reels (basic approach)
        for _ in range(3):
            await page.mouse.wheel(0, 5000)
            await page.wait_for_timeout(1000)

        # Find reel links
        anchors = await page.query_selector_all("a[href*='/reel/']")
        seen = set()

        for anchor in anchors:
            href = await anchor.get_attribute("href")
            if href and href.startswith("/reel/") and href not in seen:
                reel_url = f"https://www.instagram.com{href}"
                id = href.strip("/").split("/")[-1]
                seen.add(href)

                # Click reel or extract video link if visible
                await page.goto(reel_url)
                await page.wait_for_timeout(1000)

                video_url = await get_video_url(page)
                thumbnail_url = await get_thumbnail_url(page)
                caption = await get_caption_text(page)

                reels.append(Reel(
                    id=id,
                    reel_url=reel_url,
                    video_url=video_url,
                    thumbnail_url=thumbnail_url,
                    caption=caption,
                    posted_at=None,     # Instagram hides this in public view
                    views=None,
                    likes=None,
                    comments=None
                ))

                if len(reels) >= limit:
                    break

        await browser.close()
        return reels

async def get_video_url(page):
    try:
        video = await page.query_selector("video")
        return await video.get_attribute("src")
    except:
        return None

async def get_thumbnail_url(page):
    try:
        img = await page.query_selector("img")
        return await img.get_attribute("src")
    except:
        return None

async def get_caption_text(page):
    try:
        caption = await page.query_selector("span")
        return await caption.inner_text()
    except:
        return None