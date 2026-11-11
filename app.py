import os
import uuid
from flask import Flask, request, render_template_string, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# Listes en mémoire pour stocker les connexions et les UUIDs générés
connections = []
generated_users = []

@app.route('/')
def dashboard():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Tunnel Tracker Dashboard</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { font-family: Arial, sans-serif; padding: 15px; background: #0f172a; color: #f8fafc; }
            h2, h3 { color: #38bdf8; }
            table { width: 100%; border-collapse: collapse; margin-top: 15px; background: #1e293b; border-radius: 8px; overflow: hidden; margin-bottom: 25px; }
            th, td { padding: 12px; text-align: left; border-bottom: 1px solid #334155; font-size: 14px; }
            th { background: #0284c7; color: white; }
            .btn { display: inline-block; background: #0ea5e9; color: white; padding: 10px 15px; text-decoration: none; border-radius: 5px; font-weight: bold; margin-bottom: 20px; }
            .code-box { background: #0f172a; padding: 6px; border-radius: 4px; word-break: break-all; font-family: monospace; font-size: 12px; border: 1px solid #334155; }
        </style>
    </head>
    <body>
        <h2>Tableau de bord - Suivi des Tunnels</h2>
        <p>Statut du serveur : <strong>Actif</strong></p>
        
        <a class="btn" href="/create-user">+ Générer un nouvel UUID unique</a>

        <h3>Identifiants uniques (UUID) créés :</h3>
        <table>
            <tr>
                <th>Nom</th>
                <th>UUID Unique</th>
            </tr>
            {% if generated_users %}
                {% for u in generated_users %}
                <tr>
                    <td>{{ u.name }}</td>
                    <td><div class="code-box">{{ u.uuid }}</div></td>
                </tr>
                {% endfor %}
            {% else %}
                <tr><td colspan="2" style="text-align: center; color: #94a3b8;">Aucun UUID généré pour l'instant.</td></tr>
            {% endif %}
        </table>

        <h3>Connexions en direct :</h3>
        <table>
            <tr>
                <th>UUID / Tunnel</th>
                <th>Adresse IP</th>
                <th>Appareil</th>
                <th>Dernière Activité</th>
            </tr>
            {% if connections %}
                {% for c in connections %}
                <tr>
                    <td>{{ c.tunnel_id }}</td>
                    <td>{{ c.ip }}</td>
                    <td>{{ c.ua }}</td>
                    <td>{{ c.time }}</td>
                </tr>
                {% endfor %}
            {% else %}
                <tr><td colspan="4" style="text-align: center; color: #94a3b8;">Aucune connexion active pour le moment.</td></tr>
            {% endif %}
        </table>
    </body>
    </html>
    """
    return render_template_string(html, connections=connections, generated_users=generated_users)

@app.route('/create-user')
def create_user():
    # Génère un UUID unique universel
    new_uuid = str(uuid.uuid4())
    user_name = f"Utilisateur_{len(generated_users) + 1}"
    generated_users.insert(0, {"name": user_name, "uuid": new_uuid})
    return redirect(url_for('dashboard'))

@app.route('/track/<tunnel_id>')
def track(tunnel_id):
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    ua = request.headers.get('User-Agent', 'Inconnu')
    time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    conn_data = {"tunnel_id": tunnel_id, "ip": ip, "ua": ua, "time": time_str}
    connections.insert(0, conn_data)
    
    if len(connections) > 50:
        connections.pop()
        
    return {"status": "success", "uuid": tunnel_id, "recorded_at": time_str}

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
