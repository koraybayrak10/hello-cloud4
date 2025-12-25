from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2, os

app = Flask(__name__)
CORS(app)

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://hello_cloud4_db_user:9NiN0cKXfCJOvVIukoYGV3eu28S2nUS4@dpg-d56feb0gjchc7390o9f0-a.oregon-postgres.render.com/hello_cloud4_db"
)

def connect_db():
    return psycopg2.connect(DATABASE_URL)

@app.route("/ziyaretciler", methods=["GET", "POST"])
def ziyaretciler():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS ziyaretciler (id SERIAL PRIMARY KEY, isim TEXT, mesaj TEXT)")

    if request.method == "POST":
        data = request.json
        isim = data.get("isim")
        mesaj = data.get("mesaj")
        if isim and mesaj:
            cur.execute("INSERT INTO ziyaretciler (isim, mesaj) VALUES (%s, %s)", (isim, mesaj))
            conn.commit()

    cur.execute("SELECT isim, mesaj FROM ziyaretciler ORDER BY id DESC LIMIT 10")
    isimler = [{"isim": row[0], "mesaj": row[1]} for row in cur.fetchall()]

    cur.close()
    conn.close()

    return jsonify(isimler)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
