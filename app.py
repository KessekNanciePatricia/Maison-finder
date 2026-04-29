from flask import Flask, request, render_template_string
import sqlite3
import os

app = Flask(__name__)

# 🔥 DATABASE
def init_db():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS demandes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT,
            ville TEXT,
            budget TEXT,
            maison TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# 🌐 FRONTEND
html = """
<!DOCTYPE html>
<html>
<head>
<title>Maison Finder</title>
<style>
body{font-family:Arial;background:#f4f4f4;padding:30px;}
.box{max-width:500px;margin:auto;background:white;padding:25px;border-radius:15px;box-shadow:0 0 10px gray;}
input,select{width:100%;padding:12px;margin:8px 0;}
button{width:100%;padding:12px;background:green;color:white;border:none;cursor:pointer;}
h1{text-align:center;}
a{text-align:center;display:block;margin-top:10px;}
</style>
</head>
<body>

<div class="box">
<h1>🏠 Maison Finder</h1>

<form action="/save" method="post">
<input name="nom" placeholder="Nom" required>
<input name="ville" placeholder="Ville" required>
<input name="budget" placeholder="Budget" required>

<select name="maison">
<option>Studio</option>
<option>Appartement</option>
<option>Villa</option>
<option>Duplex</option>
</select>

<button type="submit">Envoyer</button>
</form>

<a href="/stats">Voir les demandes</a>

</div>

</body>
</html>
"""

# 🏠 HOME
@app.route("/")
def home():
    return render_template_string(html)

# 💾 SAVE DATABASE
@app.route("/save", methods=["POST"])
def save():
    nom = request.form["nom"]
    ville = request.form["ville"]
    budget = request.form["budget"]
    maison = request.form["maison"]

    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("INSERT INTO demandes (nom, ville, budget, maison) VALUES (?, ?, ?, ?)",
              (nom, ville, budget, maison))
    conn.commit()
    conn.close()

    return "<h2>✅ Enregistré avec succès</h2><a href='/'>Retour</a>"

# 📊 STATS
@app.route("/stats")
def stats():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("SELECT * FROM demandes")
    rows = c.fetchall()
    conn.close()

    result = "<h2>📊 Demandes</h2>"

    for r in rows:
        result += f"<p>👤 {r[1]} - {r[2]} - {r[3]} - {r[4]}</p>"

    result += "<br><a href='/'>Retour</a>"
    return result


# 🚀 RUN
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)