import random
from faker import Faker

# -----------------------------
# Random Seed
# -----------------------------
SEED = 42
random.seed(SEED)
fake = Faker("en_US")
Faker.seed(SEED)

# -----------------------------
# Dataset Sizes
# -----------------------------
NUM_CUSTOMERS = 5000
NUM_PRODUCTS = 500
NUM_ORDERS = 30000
NUM_PAYMENTS = 30000
NUM_REFUNDS = 4000
NUM_SUPPORT_TICKETS = 8000
NUM_WEBSITE_EVENTS = 75000

# -----------------------------
# Product Categories
# -----------------------------
PRODUCT_CATEGORIES = [
    "Electronics",
    "Home",
    "Fashion",
    "Sports",
    "Books",
    "Beauty",
    "Grocery",
    "Automotive",
    "Toys",
    "Office"
]

# -----------------------------
# Payment Methods
# -----------------------------
PAYMENT_METHODS = [
    "Credit Card",
    "Debit Card",
    "PayPal",
    "Apple Pay",
    "Google Pay",
    "Bank Transfer"
]

# -----------------------------
# Order Status
# -----------------------------
ORDER_STATUS = [
    "Completed",
    "Delivered",
    "Cancelled",
    "Returned",
    "Processing",
    "Shipped"
]

# -----------------------------
# Ticket Priority
# -----------------------------
TICKET_PRIORITY = [
    "Low",
    "Medium",
    "High",
    "Critical"
]

# -----------------------------
# Ticket Status
# -----------------------------
TICKET_STATUS = [
    "Open",
    "In Progress",
    "Resolved",
    "Closed"
]

# -----------------------------
# Website Events
# -----------------------------
WEBSITE_EVENTS = [
    "Page View",
    "Product View",
    "Search",
    "Add To Cart",
    "Checkout",
    "Purchase"
]

# -----------------------------
# US Regions
# -----------------------------
US_REGIONS = [
    "Northeast",
    "Midwest",
    "South",
    "West"
]