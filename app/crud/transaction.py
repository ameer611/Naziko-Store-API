from app.models import Transaction


def create_transaction_on_db(db, user_id, transaction):
    transaction_db = Transaction(
        user_id=user_id,
        amount=transaction.get("amount"),
        description=transaction.get("description"),
        date=transaction.get("date"),
        order_id=transaction.get("order_id"),
        image_url=transaction.get("image_url")
    )
    db.add(transaction_db)
    db.commit()
    db.refresh(transaction_db)
    return transaction_db

def get_transactions_from_db(db, user_id):
    if not user_id:
        return None
    transactions = db.query(Transaction).filter(Transaction.user_id==user_id).order_by(Transaction.date.desc()).all()
    if not transactions:
        return None
    return transactions



###########################################
# Admin CRUD Operations
###########################################
def get_transactions_from_db_for_admin(db):
    transactions = db.query(Transaction).order_by(Transaction.created_at.desc()).all()
    if not transactions:
        return None
    return transactions

def get_transaction_by_id(db, transaction_id):
    transaction = db.query(Transaction).filter(Transaction.id==transaction_id).first()
    if not transaction:
        return None
    return transaction

def update_transaction_to_valid(db, transaction_id):
    transaction = db.query(Transaction).filter(Transaction.id==transaction_id).first()
    if not transaction:
        return None
    transaction.is_approved = True
    db.commit()
    return transaction