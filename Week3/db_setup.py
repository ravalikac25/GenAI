import sqlite3
import random
import logging
import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

def init_db():
    logger.info("Starting database initialization...")
    conn = sqlite3.connect("sample.db")
    cur = conn.cursor()

    logger.info("Dropping old tables (if they exist)...")
    cur.executescript("""
    DROP TABLE IF EXISTS orders;
    DROP TABLE IF EXISTS products;
    DROP TABLE IF EXISTS users;
    """)

    logger.info("Creating tables...")
    cur.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER,
        city TEXT
    )
    """)
    cur.execute("""
    CREATE TABLE products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT,
        price REAL
    )
    """)
    cur.execute("""
    CREATE TABLE orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        product_id INTEGER,
        quantity INTEGER,
        order_date TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (product_id) REFERENCES products (id)
    )
    """)

    # Insert users
    users = [
        ("Alice", 30, "New York"),
        ("Bob", 25, "Chicago"),
        ("Charlie", 35, "San Francisco"),
        ("Diana", 28, "Boston"),
        ("Ethan", 40, "Austin"),
        ("Fiona", 32, "Seattle"),
        ("George", 45, "Denver"),
        ("Hannah", 27, "Miami"),
    ]
    cur.executemany("INSERT INTO users (name, age, city) VALUES (?, ?, ?)", users)
    logger.info(f"Inserted {len(users)} users.")

    # Insert products
    products = [
        ("Laptop", "Electronics", 1200.00),
        ("Headphones", "Electronics", 150.00),
        ("Coffee Maker", "Home", 80.00),
        ("Desk Chair", "Office", 250.00),
        ("Notebook", "Stationery", 5.00),
        ("Water Bottle", "Lifestyle", 20.00),
        ("Backpack", "Lifestyle", 60.00),
        ("Smartphone", "Electronics", 900.00)
    ]
    cur.executemany("INSERT INTO products (name, category, price) VALUES (?, ?, ?)", products)
    logger.info(f"Inserted {len(products)} products.")

    # Insert orders
    logger.info("Generating random orders...")
    for i in range(50):
        user_id = random.randint(1, len(users))
        product_id = random.randint(1, len(products))
        quantity = random.randint(1, 5)
        days_ago = random.randint(1, 120)
        order_date = (datetime.datetime.now() - datetime.timedelta(days=days_ago)).strftime("%Y-%m-%d")
        cur.execute(
            "INSERT INTO orders (user_id, product_id, quantity, order_date) VALUES (?, ?, ?, ?)",
            (user_id, product_id, quantity, order_date)
        )
        logger.info(f"Order {i+1}: user_id={user_id}, product_id={product_id}, qty={quantity}, date={order_date}")

    conn.commit()
    conn.close()
    logger.info("Database initialized successfully with users, products, and 50 random orders.")

if __name__ == "__main__":
    init_db()
