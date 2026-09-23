from app.database import AsyncSessionLocal
from sqlalchemy import select
import asyncio
from sqlalchemy import func
from app.models.product import Product
from app.models.order import Order
from app.models.category import Category


async def count_products():
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(func.count(Product.id)))
        return result.scalar()
async def count_orders():
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(func.count(Order.id)))
        return result.scalar()
async def count_categories():
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(func.count(Category.id)))
        return result.scalar()

async def get_stats():
    products, orders, categories = await asyncio.gather(
        count_products(),
        count_orders(),
        count_categories(),
    )
    return {"products": products, "orders": orders, "categories": categories}