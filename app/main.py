from fastapi import FastAPI

from app.api.v1 import (auth_routes,
                        product_routes,
                        user_routes,
                        cart_routes,
                        shipment_routes,
                        order_routes,
                        transaction_routes,
                        percentage_routes)
from app.api.v1.admin_routes import (product_routes as admin_product_routes,
                                     percentage_routes as admin_percentage_routes,
                                     user_routes as admin_user_routes,
                                     shipment_routes as admin_shipment,
                                     order_routes as admin_order_routes,
                                     transaction_routes as admin_transaction_routes)
from app.db.init_db import init_db

main_app = FastAPI(
    title="Naziko Store API",
    description="This is a simple API for Naziko Store",
    version="0.1.0",
    docs_url="/",
    redoc_url=None,
    prefix="/api"
)

async def startup_event():
    await init_db()

main_app.add_event_handler("startup", startup_event)

##############################################
# Public routes
##############################################
main_app.include_router(auth_routes.router, prefix="/v1/auth", tags=["auth"])
main_app.include_router(product_routes.router, prefix="/v1/products", tags=["products"])
main_app.include_router(user_routes.router, prefix="/v1/profile", tags=["profile"])
main_app.include_router(cart_routes.router, prefix="/v1/cart", tags=["cart"])
main_app.include_router(shipment_routes.router, prefix="/v1/shipment", tags=["shipment"])
main_app.include_router(order_routes.router, prefix="/v1/order", tags=["order"])
main_app.include_router(transaction_routes.router, prefix="/v1/transaction", tags=["transaction"])

##############################################
# Admin routes
##############################################
main_app.include_router(admin_product_routes.router, prefix="/v1/admin", tags=["admin/products"])
main_app.include_router(admin_percentage_routes.router, prefix="/v1/admin", tags=["admin/percentage"])
main_app.include_router(admin_user_routes.router, prefix="/v1/admin", tags=["admin/users"])
main_app.include_router(admin_shipment.router, prefix="/v1/admin", tags=["admin/shipment"])
main_app.include_router(admin_order_routes.router, prefix="/v1/admin", tags=["admin/orders"])
main_app.include_router(admin_transaction_routes.router, prefix="/v1/admin", tags=["admin/transactions"])



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(main_app)
