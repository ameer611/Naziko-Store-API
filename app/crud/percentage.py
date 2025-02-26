from app.models.transaction import Percentage


def create_percentage_on_db(db, percentage):
    """Create a new percentage on the database."""
    percentage = Percentage(**percentage.dict())
    db.add(percentage)
    db.commit()
    db.refresh(percentage)
    return percentage

def get_percentages_from_db(db):
    """Get all percentages from the database."""
    percentages = db.query(Percentage).all()
    for percentage in percentages:
        if percentage.description is None:
            percentage.description = "No description available"
        if percentage.percentage is None:
            percentage.percentage = 0.0
    return percentages


def update_percentage_on_db(id, db, percentage_update):
    """Update a percentage in the database, allowing updates to either field."""

    percentage = db.query(Percentage).filter(Percentage.id == id).first()
    if not percentage:
        return None  # Return None if no record is found

    update_data = percentage_update.dict(exclude_unset=True)  # Exclude fields that were not provided

    if not update_data:
        return {"message": "No changes provided."}  # Handle empty update requests

    db.query(Percentage).filter(Percentage.id == id).update(update_data)
    db.commit()

    return {"message": "Percentage updated successfully."}