from fastapi import FastAPI

from app.api.v1 import auth_routes, product_routes, user_routes, cart_routes, shipment_routes, order_routes
from app.api.v1.admin_routes import product_routes as admin_product_routes, percentage, \
    user_routes as admin_user_routes, shipment_routes as admin_shipment
from app.db.init_db import init_db

main_app = FastAPI(
    title="Naziko Store API",
    description="This is a simple API for Naziko Store",
    version="0.1.0",
    docs_url="/",
    redoc_url=None,
    prefix="/api"
)

init_db()
main_app.include_router(auth_routes.router, prefix="/v1/auth", tags=["auth"])
main_app.include_router(product_routes.router, prefix="/v1/products", tags=["products"])
main_app.include_router(user_routes.router, prefix="/v1/profile", tags=["profile"])
main_app.include_router(cart_routes.router, prefix="/v1/cart", tags=["cart"])
main_app.include_router(shipment_routes.router, prefix="/v1/shipment", tags=["shipment"])
main_app.include_router(order_routes.router, prefix="/v1/order", tags=["order"])

##############################################
# Admin routes
##############################################
main_app.include_router(admin_product_routes.router, prefix="/v1/admin", tags=["admin/products"])
main_app.include_router(percentage.router, prefix="/v1/admin", tags=["admin/percentage"])
main_app.include_router(admin_user_routes.router, prefix="/v1/admin", tags=["admin/users"])
main_app.include_router(admin_shipment.router, prefix="/v1/admin", tags=["admin/shipment"])
