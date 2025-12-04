import sqlite3

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                quantity INTEGER NOT NULL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY,
                product_name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL,
                total REAL NOT NULL
            )
        """)
        self.conn.commit()

    def add_product(self, name, price, quantity):
        self.cursor.execute("INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)", (name, price, quantity))
        self.conn.commit()

    def get_products(self):
        self.cursor.execute("SELECT * FROM products")
        return self.cursor.fetchall()

    def update_product_quantity(self, name, quantity):
        self.cursor.execute("UPDATE products SET quantity = ? WHERE name = ?", (quantity, name))
        self.conn.commit()

    def add_sale(self, product_name, quantity, price, total):
        self.cursor.execute("INSERT INTO sales (product_name, quantity, price, total) VALUES (?, ?, ?, ?)", (product_name, quantity, price, total))
        self.conn.commit()

    def get_sales(self):
        self.cursor.execute("SELECT * FROM sales")
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()