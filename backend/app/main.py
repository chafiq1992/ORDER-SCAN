from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import datetime as dt, asyncio

from .database import get_db, engine
from .models import Base
from .settings import settings
from .crud import get_scan, create_scan, tag_summary
from .shopify import find_order
from .sheets import append_row

app = FastAPI(title="Order Scanner API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/", StaticFiles(directory="../frontend/dist", html=True), name="static")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

def _primary_tag(tags: str):
    lowered = tags.lower()
    for t in ["big", "k", "12livery", "12livrey", "fast", "oscario", "sand"]:
        if t in lowered:
            return t
    return ""

@app.post("/api/scan")
async def scan(barcode: str, db=Depends(get_db)):
    digits = "".join(filter(str.isdigit, barcode)).lstrip("0")
    if len(digits) == 0 or len(digits) > settings.MAX_DIGITS:
        raise HTTPException(400, "Invalid barcode")

    order = f"#{digits}"
    if await get_scan(db, order):
        return {"result": "⚠️ Already Scanned", "order": order, "tag": ""}

    data = await find_order(order)
    if not data:
        return {"result": "❌ Not Found", "order": order, "tag": ""}

    if data["fulfillment"] == "unfulfilled" and not data["tags"].strip():
        return {"result": "❌ Unfulfilled / No Tag", "order": order, "tag": ""}

    await create_scan(
        db,
        order_name=order,
        tags=data["tags"],
        fulfillment=data["fulfillment"],
        status=data["status"],
        store=data["store"],
        result=data["result"],
    )

    # Optional Google Sheet
    append_row(
        [
            dt.datetime.now().isoformat(sep=" ", timespec="seconds"),
            order,
            data["tags"],
            data["fulfillment"],
            data["status"],
            data["store"],
            data["result"],
        ]
    )

    return {"result": data["result"], "order": order, "tag": _primary_tag(data["tags"])}

@app.get("/api/tag-summary")
async def get_summary(db=Depends(get_db)):
    return await tag_summary(db)
