from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# 💾 DATABASE
def import os

if not os.path.exists("data.db"):
    init_db():
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

# 🌐 FRONTEND (AMÉLIORÉ)
html = """
<!DOCTYPE html>
<html>
<head>
<title>Maison Finder</title>

<link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css"/>

<style>
body{
font-family:Arial;
background:linear-gradient(135deg,#74ebd5,#ACB6E5);
margin:0;
padding:20px;
}

.container{
max-width:900px;
margin:auto;
background:white;
padding:20px;
border-radius:15px;
box-shadow:0 5px 20px rgba(0,0,0,0.2);
}

form{
margin-bottom:20px;
}

input,select{
width:100%;
padding:10px;
margin:5px 0;
border-radius:8px;
border:1px solid #ccc;
}

button{
width:100%;
padding:10px;
background:#4CAF50;
color:white;
border:none;
cursor:pointer;
border-radius:8px;
}

button:hover{
background:#45a049;
}

.grid{
display:grid;
grid-template-columns:repeat(auto-fit,minmax(220px,1fr));
gap:10px;
margin-top:20px;
}

.card{
background:#f9f9f9;
padding:10px;
border-radius:10px;
box-shadow:0 3px 10px rgba(0,0,0,0.1);
}

.card img{
width:100%;
height:120px;
object-fit:cover;
border-radius:10px;
}

#map{
height:250px;
margin-top:20px;
border-radius:10px;
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

<h2>🏡 Maisons disponibles</h2>

<div class="grid">
{% for m in data %}
<div class="card">
<img src="https://source.unsplash.com/400x300/?house,home,building">
<h3>{{ m[3] }}</h3>
<p>👤 {{ m[1] }}</p>
<p>📍 {{ m[2] }}</p>
<p>💰 {{ m[3] }}</p>
</div>
{% endfor %}
</div>

<!-- 🗺️ CARTE -->
<div id="map"></div>

</div>

<script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
<script>
try {
    var map = L.map('map').setView([4.05, 9.7], 12);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap'
    }).addTo(map);

    L.marker([4.05, 9.7]).addTo(map)
        .bindPopup("Maison disponible ici");
} catch (e) {
    console.log("Erreur carte :", e);
}
</script>

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

    return "<h2>✅ Envoyé avec succès</h2><a href='/'>Retour</a>"

# 🚀 RUN
if __name__ == "__main__":
 import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)