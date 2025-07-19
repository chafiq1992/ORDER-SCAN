import aiohttp, asyncio, base64, datetime as dt
from .settings import settings

def _auth(k, p):
    token = base64.b64encode(f"{k}:{p}".encode()).decode()
    return {"Authorization": f"Basic {token}"}

async def _fetch(session, store, url):
    async with session.get(url, headers=_auth(store['api_key'], store['password'])) as r:
        if r.status != 200:
            return None
        data = await r.json()
        return data.get("orders", [None])[0]

async def find_order(order_name: str):
    cutoff = dt.datetime.utcnow() - dt.timedelta(days=settings.ORDER_CUTOFF_DAYS)
    async with aiohttp.ClientSession() as session:
        tasks = []
        for s in settings.shopify_stores:
            url = f"https://{s['domain']}/admin/api/2024-04/orders.json?name={order_name}"
            tasks.append(_fetch(session, s, url))
        responses = await asyncio.gather(*tasks)

    best = None
    for s, resp in zip(settings.shopify_stores, responses):
        if not resp:
            continue
        created = dt.datetime.fromisoformat(resp['created_at'].rstrip('Z'))
        if created < cutoff:
            continue
        candidate = {
            "tags": resp.get("tags", ""),
            "fulfillment": resp.get("fulfillment_status") or "unfulfilled",
            "status": "closed" if resp.get("cancelled_at") else "open",
            "store": s['name'],
            "result": "⚠️ Cancelled" if resp.get("cancelled_at") else (
                      "❌ Unfulfilled" if resp.get("fulfillment_status") != "fulfilled" else "✅ OK"),
            "created": created
        }
        if not best or candidate["created"] > best["created"]:
            best = candidate
    return best
