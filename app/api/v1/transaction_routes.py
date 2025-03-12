import os
import shutil
from datetime import datetime
from typing import List
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.alibaba_scraper.products_scraper import delete_file_from_server
from app.core.security import get_current_user
from app.crud.authentication import get_user_by_phone
from app.crud.order import get_order_by_id
from app.crud.transaction import create_transaction_on_db, get_transactions_from_db
from app.crud.user import get_customer_by_id_from_db
from app.db.base import get_db
from app.schemas.transaction import TransactionResponse
from app.service.telegram import send_photo_and_get_file_link

router = APIRouter()

UPLOAD_FOLDER = os.getenv("UPLOAD_TRANSACTIONS_FOLDER", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@router.post("/create-transaction", response_model=TransactionResponse, status_code=201)
async def create_transaction_endpoint(
        transaction_image: UploadFile,
        amount: float = Form(..., gt=0),
        description: str = Form(None, max_length=255),
        date: datetime = Form(...),
        order_id: int = Form(..., gt=0),
        user: dict = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
):
    user_db = await get_customer_by_id_from_db(db, int(user["user_id"]))
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found.")

    order_db = await get_order_by_id(db, user_db.id, order_id)
    if not order_db:
        raise HTTPException(status_code=404, detail="Order not found.")

    # Validate file type (allow only images)
    allowed_extensions = [".jpg", ".jpeg", ".png", ".pdf"]
    file_extension = os.path.splitext(transaction_image.filename)[-1].lower()

    if file_extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Invalid file type. Only JPG, PNG, and PDF files are allowed.")

    # Generate a unique filename to prevent overwriting
    unique_filename = f"{uuid4().hex}{file_extension}"
    file_path = os.path.join(UPLOAD_FOLDER, unique_filename)

    # Save the file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(transaction_image.file, buffer)

    # Upload the file to Telegram
    telegram_file_link = send_photo_and_get_file_link(file_path)
    if not telegram_file_link:
        raise HTTPException(status_code=400, detail="Error uploading file to Telegram.")

    # Ensure that datetime is timezone-naive
    date_naive = date.replace(tzinfo=None)

    # Create transaction in the database
    transaction_data = {
        "user_id": user_db.id,
        "amount": amount,
        "description": description,
        "date": date_naive,
        "order_id": order_id,
        "image_url": telegram_file_link,
    }

    transaction_db = await create_transaction_on_db(db, user_db.id, transaction_data)
    if not transaction_db:
        raise HTTPException(status_code=400, detail="Error creating transaction.")

    product_links = [i.product_link for i in transaction_db.order.order_items]

    # Corrected message format (not a tuple)
    message = f"🆕 *New Transaction Received* 🆕\n"\
        f"🆔Transaction ID: {transaction_db.id},\n"\
        f"👤Customer fullname: {user_db.fullname},\n"\
        f"📞Customer phone number: {user_db.phone_number},\n"\
        f"📦Order ID: {order_id},\n"\
        f"💲Order amount: {order_db.total_price},\n"\
        f"💰Transaction Amount: {amount},\n"\
        f"📝Description: {description},\n"\
        f"📅Date: {date.strftime('%d.%m.%Y %H:%M')}\n"\
        f"🛒Product Links: \n🔗{'\n🔗'.join(product_links)}\n"

    send_photo_and_get_file_link(file_path, message=message, chat_id=os.getenv("ADMIN_CHAT_ID"))

    delete_file_from_server(file_path)
    return TransactionResponse.model_validate(transaction_db)

@router.get("/transactions", response_model=List[TransactionResponse], status_code=200)
async def get_all_transactions(user: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    user_db = await get_user_by_phone(db, user.get("phone_number"))
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found.")

    transactions = await get_transactions_from_db(db, user_db.id)
    if not transactions:
        raise HTTPException(status_code=404, detail="Transactions not found.")

    return transactions