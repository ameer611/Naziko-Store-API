from fastapi import HTTPException

from app.core.security import verify_password, hash_password
from app.models import User


def change_user_info_on_db(db, user_id, changed_info):
    """Changes user info in the database."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    update_data = changed_info.dict(exclude_unset=True)
    if not update_data:
        return {"message": "No changes provided."}
    db.query(User).filter(User.id == user_id).update(update_data)
    db.commit()
    return db.query(User).filter(User.id == user_id).first()


def change_user_password_on_db(db, user_id, changed_info):
    """Changes user password in the database."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    user.password_hash = hash_password(changed_info.new_password)
    db.commit()
    return db.query(User).filter(User.id == user_id).first()


def check_passwords(old_password, user_id, db):
    """Check if the old password is correct."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(old_password, user.password_hash):
        return False
    return True

def change_phone_number_on_db(db, user_id, phone_number):
    """Change phone number in the database."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    user.phone_number = phone_number
    db.commit()
    return db.query(User).filter(User.id == user_id).first()


########################################
# Admin functions
########################################
def get_customers_from_db(db, user):
    """Get all customers from the database."""
    return db.query(User).filter(User.is_superuser==False).all()

def get_customer_by_id_from_db(db, customer_id):
    """Get a customer by ID from the database."""
    return db.query(User).filter(User.id==customer_id).first()

def change_customer_password_on_db(db, customer, new_password):
    """Change customer password in the database."""
    customer.password_hash = hash_password(new_password)
    db.commit()
    return db.query(User).filter(User.id == customer.id).first()

def delete_customer_from_db(db, customer):
    """Delete a customer from the database."""
    db.delete(customer)
    db.commit()
    return {"message": "Customer deleted successfully"}