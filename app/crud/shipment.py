from app.models import ShipmentType


def create_shipment_type_on_db(db, shipment):
    existing_shipment = db.query(ShipmentType).filter(ShipmentType.title == shipment.title).first()
    if existing_shipment:
        return None
    shipment_db = ShipmentType(**shipment.dict())
    db.add(shipment_db)
    db.commit()
    db.refresh(shipment_db)
    return shipment_db

def get_shipments_from_db(db):
    return db.query(ShipmentType).all()

def get_shipment_by_id(db, shipment_id):
    shipment_db = db.query(ShipmentType).filter(ShipmentType.id == shipment_id).first()
    if not shipment_db:
        return None
    return shipment_db

def update_shipment_on_db(db, shipment_db, shipment):
    updated_shipment = shipment.dict(exclude_unset=True)

    # Retrieve the existing shipment
    existing_shipment = db.query(ShipmentType).filter(ShipmentType.id == shipment_db.id).first()

    if not existing_shipment:
        return None  # Or raise an exception

    # Apply the updates manually
    for key, value in updated_shipment.items():
        setattr(existing_shipment, key, value)

    db.commit()
    db.refresh(existing_shipment)
    return existing_shipment
