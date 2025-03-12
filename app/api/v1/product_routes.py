import os
import shutil
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from app.alibaba_scraper.products_scraper import (
    get_product_by_link_from_website, get_product_variants,
    search_product_by_name_from_website, get_product_comments,
    delete_file_from_server, search_product_by_image_from_website
)
from app.core.security import get_current_user
from app.crud.authentication import get_user_by_phone
from app.crud.product import (
    get_products_from_db, get_product_from_db_if_exists, save_product_on_db,
    update_product_add_variants_to_db_product
)
from app.db.base import get_db
from app.schemas.product import DatabaseProductResponse, ProductLink, OnlineProductResponse

router = APIRouter()


@router.get("/products", response_model=list[DatabaseProductResponse])
async def get_products(db: AsyncSession = Depends(get_db)):
    products = await get_products_from_db(db)
    return products


@router.post("/product-details", response_model=OnlineProductResponse)
async def get_product(product_link: ProductLink, user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if not user:
        raise HTTPException(status_code=401, detail="You need to be logged in to perform this action.")
    product_db = await get_product_from_db_if_exists(db, product_link.product_link)
    if product_db:
        return product_db
    product = get_product_by_link_from_website(product_link.product_link)  # No await here
    if not product:
        return {"message": "Product not found."}
    saved_product = await save_product_on_db(db, product, product_link.product_link)
    if not saved_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return saved_product


@router.post("/product-variants")
async def get_product_variants_route(product_link: ProductLink, user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if not user:
        raise HTTPException(status_code=401, detail="You need to be logged in to perform this action.")
    product_db = await get_product_from_db_if_exists(db, product_link.product_link)

    if not product_db:
        return {"message": "Product not found."}

    if product_db.variants:
        return product_db.variants
    variants = get_product_variants(product_link.product_link)  # No await here
    if not variants:
        return {"message": "No variants found."}
    variants_db = await update_product_add_variants_to_db_product(db, variants, product_link.product_link)
    if not variants_db:
        raise HTTPException(status_code=404, detail="Product not found")
    return variants_db


@router.get("/search-by-title", response_model=list[dict])
async def search_product_by_title(product_name: str, page_number: int = 1, user=Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="You need to be logged in to perform this action.")

    products = search_product_by_name_from_website(product_name, page=page_number)  # No await here
    return products


# Ensure the upload folder exists
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@router.post("/search-product-by-image")
async def search_product_by_image(file: UploadFile = File(...), user=Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="You need to be logged in to perform this action.")

    # Validate file type (allow only images)
    allowed_extensions = {".jpg", ".jpeg", ".png", ".webp"}
    file_extension = os.path.splitext(file.filename)[-1].lower()

    if file_extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Invalid file type. Only JPG, PNG, and WEBP images are allowed.")

    # Generate a unique filename to prevent overwriting
    unique_filename = f"{uuid4().hex}{file_extension}"
    file_path = os.path.join(UPLOAD_FOLDER, unique_filename)

    # Save the file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    products = search_product_by_image_from_website(file_path)  # No await here
    response = delete_file_from_server(file_path)  # No await here
    if products:
        return products
    return {"message": "Error deleting file."}


@router.post("/product-reviews", response_model=dict)
async def get_product_reviews(product_link: ProductLink, user=Depends(get_current_user)):
    reviews = get_product_comments(product_link.product_link)  # No await here
    if not reviews:
        return {"message": "No reviews found."}
    return reviews