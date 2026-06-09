import sqlite3
from flask import Flask, render_template,request,redirect

app = Flask(__name__)

conn =sqlite3.connect("shop.db",timeout=10)
cursor=conn.cursor()


cursor.execute("""

CREATE TABLE IF NOT EXISTS products(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT,

    category TEXT,

    quantity INTEGER,

    price INTEGER

)

""")

conn.commit()
conn.close()


conn = sqlite3.connect("shop.db",timeout=10)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS customers(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    phone TEXT,
    email TEXT,
    total_purchase INTEGER,
    status TEXT
)
""")

conn.commit()
conn.close()


conn = sqlite3.connect("shop.db",timeout=10)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS settings(
    id INTEGER PRIMARY KEY,
    shop_name TEXT,
    owner_name TEXT,
    phone TEXT,
    dark_mode INTEGER,
    notifications INTEGER,
    currency TEXT
)
""")

conn.commit()
conn.close()




@app.route("/")
def home():
    return render_template("index.html")


# ADD PRODUCT
@app.route("/products", methods=["GET", "POST"])
def add_product():

    if request.method == "POST":

        name = request.form["name"]
        category = request.form["category"]
        quantity = request.form["quantity"]
        price = request.form["price"]

        conn = sqlite3.connect("shop.db",timeout=10)
        cursor = conn.cursor()

        cursor.execute("""

        INSERT INTO products(name, category, quantity, price)

        VALUES(?,?,?,?)

        """, (name, category, quantity, price))

        conn.commit()
        conn.close()
    return render_template("products.html")




@app.route("/Sales")
def Sales():
    return render_template("Sales.html")

@app.route("/Analytics")
def Analytics():

    conn = sqlite3.connect("shop.db",timeout=10)
    cursor = conn.cursor()

    # Total products
    cursor.execute("SELECT COUNT(*) FROM products")
    total_products = cursor.fetchone()[0]

    # Total quantity
    cursor.execute("SELECT SUM(quantity) FROM products")
    total_quantity = cursor.fetchone()[0] or 0

    # Total inventory value
    cursor.execute("SELECT SUM(quantity * price) FROM products")
    total_value = cursor.fetchone()[0] or 0

    # Highest price product
    cursor.execute("""
    SELECT name, price
    FROM products
    ORDER BY price DESC
    LIMIT 1
    """)
    expensive_product = cursor.fetchone()

    # Low stock products
    cursor.execute("""
    SELECT * FROM products
    WHERE quantity < 5
    """)
    low_stock = cursor.fetchall()

    conn.close()

    return render_template(
        "Analytics.html",
        total_products=total_products,
        total_quantity=total_quantity,
        total_value=total_value,
        expensive_product=expensive_product,
        low_stock=low_stock
    )

@app.route("/Customers")
def Customers():

    conn = sqlite3.connect("shop.db",timeout=10)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM customers")
    customers = cursor.fetchall()

    print(customers)

    conn.close()

    return render_template(
        "Customers.html",
        customers=customers
    )


@app.route("/add_Customer", methods=["GET", "POST"])
def add_Customer():

    if request.method == "POST":

        name = request.form["name"]
        phone = request.form["phone"]
        email = request.form["email"]
        total_purchase = request.form["total_purchase"]
        status = request.form["status"]

        conn = sqlite3.connect("shop.db",timeout=10)
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO customers
        (name, phone, email, total_purchase, status)
        VALUES (?, ?, ?, ?, ?)
        """, (
            name,
            phone,
            email,
            total_purchase,
            status
        ))

        conn.commit()
        conn.close()

        return redirect("/Customers")

    return render_template("add_customer.html")


@app.route("/delete_Customer/<int:id>")
def delete_Customer(id):

    conn = sqlite3.connect("shop.db",timeout=10)
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM customers WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/Customers")


@app.route("/edit_Customer/<int:id>", methods=["GET", "POST"])
def edit_customer(id):

    conn = sqlite3.connect("shop.db",timeout=10)
    cursor = conn.cursor()

    if request.method == "POST":

        name = request.form["name"]
        phone = request.form["phone"]
        email = request.form["email"]
        total_purchase = request.form["total_purchase"]
        status = request.form["status"]

        cursor.execute("""
        UPDATE customers
        SET
            name=?,
            phone=?,
            email=?,
            total_purchase=?,
            status=?
        WHERE id=?
        """, (
            name,
            phone,
            email,
            total_purchase,
            status,
            id
        ))

        conn.commit()
        conn.close()

        return redirect("/Customers")

    cursor.execute(
        "SELECT * FROM customers WHERE id=?",
        (id,)
    )

    customer = cursor.fetchone()

    conn.close()

    return render_template(
        "edit_customer.html",
        customer=customer
    )

@app.route("/settings", methods=["GET", "POST"])
def settings():

    conn = sqlite3.connect("shop.db",timeout=10)
    cursor = conn.cursor()

    if request.method == "POST":

       shop_name = request.form["shop_name"]
    
       owner_name = request.form["owner_name"]
       phone = request.form["phone"]

       dark_mode = 1 if "dark_mode" in request.form else 0
       notifications = 1 if "notifications" in request.form else 0

       currency = request.form.get("currency", "INR")

       cursor.execute("DELETE FROM settings")

       cursor.execute("""
        INSERT INTO settings(
            shop_name,
            owner_name,
            phone,
            dark_mode,
            notifications,
            currency
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            shop_name,
            owner_name,
            phone,
            dark_mode,
            notifications,
            currency
        ))

    conn.commit()

    cursor.execute("SELECT * FROM settings LIMIT 1")
    setting = cursor.fetchone()

    conn.close()

    return render_template(
        "settings.html",
        setting=setting
    )


@app.route("/delete/<int:id>")
def delete(id):

    conn = sqlite3.connect("shop.db",timeout=10)

    cursor = conn.cursor()

    cursor.execute("DELETE FROM products WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect("/Vproducts")


@app.route("/Vproducts")
def Vproducts():
    conn = sqlite3.connect("shop.db",timeout=10)

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products")

    products = cursor.fetchall()

    conn.close()

    return render_template("Vproducts.html", products=products)

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):

    conn = sqlite3.connect("shop.db",timeout=10)

    cursor = conn.cursor()

    # UPDATE DATA
    if request.method == "POST":

        name = request.form["name"]
        category = request.form["category"]
        quantity = request.form["quantity"]
        price = request.form["price"]

        cursor.execute("""

        UPDATE products

        SET
        name=?,
        category=?,
        quantity=?,
        price=?

        WHERE id=?

        """, (name, category, quantity, price, id))

        conn.commit()
        conn.close()

        return redirect("/Vproducts")

    # FETCH OLD DATA
    cursor.execute(
        "SELECT * FROM products WHERE id=?",
        (id,)
    )

    product = cursor.fetchone()

    conn.close()

    return render_template(
        "edit.html",
        product=product
    )




if __name__ == "__main__":
    app.run(debug=True)