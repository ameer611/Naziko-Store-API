from enum import Enum


class Language(str, Enum):
    en = "en"
    uz = "uz"
    ru = "ru"

class OrderStatus(str, Enum):
    PENDING = "pending"          # Order placed but not yet processed
    PARTIALLY_PAID = "partially_paid"  # Order has been partially paid
    OVER_PAID = "over_paid"      # Order has been overpaid
    CONFIRMED = "confirmed"      # Order has been confirmed by the seller
    PROCESSING = "processing"    # Order is being prepared
    SHIPPED = "shipped"          # Order has been shipped
    DELIVERED = "delivered"      # Order successfully delivered
    CANCELED = "canceled"        # Order was canceled
    RETURNED = "returned"        # Customer returned the order
    REFUNDED = "refunded"        # Payment has been refunded

