from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Scan

async def get_scan(db: AsyncSession, order_name: str):
    q = await db.execute(select(Scan).where(Scan.order_name == order_name))
    return q.scalar_one_or_none()

async def create_scan(db: AsyncSession, **kwargs):
    scan = Scan(**kwargs)
    db.add(scan)
    await db.commit()
    await db.refresh(scan)
    return scan

async def tag_summary(db: AsyncSession):
    rows = await db.execute("SELECT LOWER(tags) AS t, COUNT(*) FROM scans GROUP BY t")
    return {r[0]: r[1] for r in rows}
