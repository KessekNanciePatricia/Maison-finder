from flask import Flask, request, render_template_string
import sqlite3
import os

app = Flask(__name__)

# 💾 DATABASE
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

# 🌐 FRONTEND + CARDS
html = """
<!DOCTYPE html>
<html>
<head>
<title>Maison Finder</title>

<style>
body{
font-family:Arial;
background:#f4f4f4;
margin:0;
padding:20px;
}

.container{
max-width:900px;
margin:auto;
}

form{
background:white;
padding:20px;
border-radius:10px;
margin-bottom:20px;
}

input,select{
width:100%;
padding:10px;
margin:5px 0;
}

button{
width:100%;
padding:10px;
background:green;
color:white;
border:none;
cursor:pointer;
}

.grid{
display:grid;
grid-template-columns:repeat(auto-fit,minmax(220px,1fr));
gap:10px;
}

.card{
background:white;
padding:15px;
border-radius:10px;
box-shadow:0 0 10px rgba(0,0,0,0.1);
}

.card h3{
color:green;
margin:0;
}
</style>

</head>

<body>

<div class="container">

<h1>🏠 Maison Finder</h1>

<!-- FORM -->
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

<h2>📊 Maisons disponibles</h2>

<div class="grid">
{% for m in data %}
<div class="card">
<h3>{{ m[3] }}</h3>
<p>👤 {{ m[1] }}</p>
<p>📍 {{ m[2] }}</p>
<p>💰 {{ m[3] }}</p>
</div>
{% endfor %}
</div>

</div>

</body>
</html>
"""

# 🏠 HOME
@app.route("/")
def home():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("SELECT * FROM demandes ORDER BY id DESC")
    data = c.fetchall()
    conn.close()

    return render_template_string(html, data=data)

# 💾 SAVE
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

    return """
    <h2>✅ Envoyé avec succès</h2>
    <a href='/'>Retour</a>
    """

# 🚀 RUN
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
