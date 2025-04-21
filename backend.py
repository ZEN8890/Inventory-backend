from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

# Ambil URL database dari environment variable
DATABASE_URL = os.environ.get("DATABASE_URL")

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

@app.route('/api/items', methods=['GET'])
def get_items():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id, name, barcode, quantity FROM products;')
        items = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify([
            {"id": row[0], "name": row[1], "barcode": row[2], "quantity": row[3]}
            for row in items
        ])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/items', methods=['POST'])
def add_item():
    data = request.json
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO products (name, barcode, quantity) VALUES (%s, %s, %s)',
            (data['name'], data['barcode'], data['quantity'])
        )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Item added successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id, name, barcode, quantity FROM products WHERE id = %s;', (item_id,))
        item = cur.fetchone()
        cur.close()
        conn.close()
        if item:
            return jsonify({"id": item[0], "name": item[1], "barcode": item[2], "quantity": item[3]})
        else:
            return jsonify({"error": "Item not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.json
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            'UPDATE products SET name = %s, barcode = %s, quantity = %s WHERE id = %s',
            (data['name'], data['barcode'], data['quantity'], item_id)
        )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Item updated successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('DELETE FROM products WHERE id = %s', (item_id,))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Item deleted successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
