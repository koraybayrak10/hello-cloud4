from flask import Flask, render_template_string, request, redirect
import requests
import os

app = Flask(__name__)

API_URL = os.environ.get("API_URL")

HTML = """
<!doctype html>
<html>
<head>
    <title>Mikro Hizmetli Selam!</title>
    <style>
        body { font-family: Arial; text-align: center; padding: 50px; background: #eef2f3; }
        h1 { color: #333; }
        input { padding: 10px; font-size: 16px; }
        button { padding: 10px 15px; background: #4CAF50; color: white; border: none; border-radius: 6px; cursor: pointer; }
        li { background: white; margin: 5px auto; width: 200px; padding: 8px; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>Mikro Hizmetli Selam!</h1>
    <p>Adını ve mesajını yaz</p>
    <form method="POST">
        <input type="text" name="isim" placeholder="Adını yaz" required>
        <input type="text" name="mesaj" placeholder="Mesajını yaz" required>
        <button type="submit">Gönder</button>
    </form>
    <h3>Ziyaretçiler:</h3>
    <ul>
        {% for z in isimler %}
            <li><b>{{ z["isim"] }}</b>: {{ z["mesaj"] }}</li>
        {% endfor %}
    </ul>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        isim = request.form.get("isim")
        mesaj = request.form.get("mesaj")
        requests.post(API_URL, json={"isim": isim, "mesaj": mesaj})
        return redirect("/")

    resp = requests.get(API_URL)
    isimler = resp.json() if resp.status_code == 200 else []
    return render_template_string(HTML, isimler=isimler)

