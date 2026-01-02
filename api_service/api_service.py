from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)

DATABASE_URL = os.environ.get("DATABASE_URL")

def connect_db():
    return psycopg2.connect(DATABASE_URL)

def init_db():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS ziyaretciler (
            id SERIAL PRIMARY KEY,
            isim TEXT NOT NULL,
            mesaj TEXT NOT NULL
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

@app.route("/ziyaretciler", methods=["GET", "POST"])
def ziyaretciler():
    conn = connect_db()
    cur = conn.cursor()

    if request.method == "POST":
        data = request.get_json()
        isim = data.get("isim")
        mesaj = data.get("mesaj")

        if not isim or not mesaj:
            return jsonify({"error": "isim ve mesaj zorunlu"}), 400

        cur.execute(
            "INSERT INTO ziyaretciler (isim, mesaj) VALUES (%s, %s)",
            (isim, mesaj)
        )
        conn.commit()

    cur.execute(
        "SELECT isim, mesaj FROM ziyaretciler ORDER BY id DESC LIMIT 10"
    )

    rows = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify([
        {"isim": r[0], "mesaj": r[1]} for r in rows
    ])

# uygulama başlarken tabloyu oluştur
init_db()
