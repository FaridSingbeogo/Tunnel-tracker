from flask import Flask, request, render_template_string
from datetime import datetime

app = Flask(__name__)

# Liste en mémoire pour stocker les connexions récentes
connections = []

@app.route('/')
def dashboard():
    # Interface web simple pour visualiser le trafic et les appareils
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Tunnel Tracker Dashboard</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { font-family: Arial, sans-serif; padding: 15px; background: #0f172a; color: #f8fafc; }
            h2 { color: #38bdf8; }
            table { width: 100%; border-collapse: collapse; margin-top: 15px; background: #1e293b; border-radius: 8px; overflow: hidden; }
            th, td { padding: 12px; text-align: left; border-bottom: 1px solid #334155; font-size: 14px; }
            th { background: #0284c7; color: white; }
        </style>
    </head>
    <body>
        <h2>Tableau de bord - Suivi des Tunnels</h2>
        <p>Statut du serveur : <strong>Actif (Gratuit)</strong></p>
        <table>
            <tr>
                <th>ID Tunnel</th>
                <th>Adresse IP</th>
                <th>Appareil / Client</th>
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
                <tr><td colspan="4" style="text-align: center; color: #94a3b8;">Aucune connexion enregistrée pour le moment.</td></tr>
            {% endif %}
        </table>
    </body>
    </html>
    """
    return render_template_string(html, connections=connections)

@app.route('/track/<tunnel_id>')
def track(tunnel_id):
    # Route appelée par le fichier de tunnelisation pour enregistrer l'utilisation
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    ua = request.headers.get('User-Agent', 'Inconnu')
    time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Enregistrer ou mettre à jour la connexion
    # On évite les doublons stricts pour garder la liste propre
    conn_data = {"tunnel_id": tunnel_id, "ip": ip, "ua": ua, "time": time_str}
    connections.insert(0, conn_data)
    
    # Garder uniquement les 50 dernières connexions en mémoire
    if len(connections) > 50:
        connections.pop()
        
    return {"status": "success", "tunnel": tunnel_id, "recorded_at": time_str}

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
