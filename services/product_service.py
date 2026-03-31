from db.database import get_db_connection


def get_all_products():
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM products").fetchall()
    conn.close()
    return [dict(row) for row in rows]


def create_product(name, price):
    conn = get_db_connection()
    cursor = conn.execute(
        "INSERT INTO products (name, price) VALUES (?, ?)",
        (name, price)
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()

    return {
        "id": new_id,
        "name": name,
        "price": price
    }


def update_product_full(id, name, price):
    conn = get_db_connection()

    product = conn.execute(
        "SELECT * FROM products WHERE id = ?", (id,)
    ).fetchone()

    if product is None:
        conn.close()
        return None

    conn.execute(
        "UPDATE products SET name = ?, price = ? WHERE id = ?",
        (name, price, id)
    )

    conn.commit()
    conn.close()

    return {
        "id": id,
        "name": name,
        "price": price
    }


def update_product_partial(id, name=None, price=None):
    conn = get_db_connection()

    product = conn.execute(
        "SELECT * FROM products WHERE id = ?", (id,)
    ).fetchone()

    if product is None:
        conn.close()
        return None

    updates = []
    values = []

    if name is not None:
        updates.append("name = ?")
        values.append(name)

    if price is not None:
        updates.append("price = ?")
        values.append(price)

    if not updates:
        conn.close()
        return "no_fields"

    query = f"UPDATE products SET {', '.join(updates)} WHERE id = ?"
    values.append(id)

    conn.execute(query, tuple(values))
    conn.commit()
    conn.close()

    return True


def delete_product_by_id(id):
    conn = get_db_connection()

    product = conn.execute(
        "SELECT * FROM products WHERE id = ?", (id,)
    ).fetchone()

    if product is None:
        conn.close()
        return False

    conn.execute("DELETE FROM products WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return True