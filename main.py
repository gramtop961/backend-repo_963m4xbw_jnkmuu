import os
from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from schemas import Product, Order
from database import db, create_document, get_documents

app = FastAPI(title="Sunny Online Store API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def serialize_doc(doc: dict) -> dict:
    if not doc:
        return doc
    d = {**doc}
    _id = d.pop("_id", None)
    if _id is not None:
        d["id"] = str(_id)
    # Convert datetime fields to isoformat if present
    for k, v in list(d.items()):
        try:
            import datetime
            if isinstance(v, (datetime.datetime, datetime.date)):
                d[k] = v.isoformat()
        except Exception:
            pass
    return d


@app.get("/")
def read_root():
    return {"message": "Sunny Online Store Backend is running"}


@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set",
        "database_name": "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set",
        "connection_status": "Not Connected",
        "collections": [],
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["connection_status"] = "Connected"
            try:
                response["collections"] = db.list_collection_names()[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️ Connected but Error: {str(e)[:80]}"
        else:
            response["database"] = "⚠️ Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"
    return response


# Products Endpoints
@app.get("/api/products")
def list_products(limit: int | None = None):
    try:
        docs = get_documents("product", {}, limit)
        return [serialize_doc(d) for d in docs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/products", status_code=201)
def create_product(product: Product):
    try:
        new_id = create_document("product", product)
        return {"id": new_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Orders Endpoints
@app.get("/api/orders")
def list_orders(limit: int | None = 100):
    try:
        docs = get_documents("order", {}, limit)
        return [serialize_doc(d) for d in docs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/orders", status_code=201)
def create_order(order: Order):
    try:
        new_id = create_document("order", order)
        return {"id": new_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
