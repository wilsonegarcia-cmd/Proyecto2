from flask import Flask, request, jsonify
import sqlite3
import datetime

app = Flask(__name__)
DB = 'access.db'

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY, token TEXT UNIQUE, nombre TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY, token TEXT, timestamp TEXT, resultado TEXT)''')
    # Insertar usuarios de ejemplo
    c.execute("INSERT OR IGNORE INTO usuarios (token, nombre) VALUES ('TOKEN123', 'Usuario Autorizado')")
    c.execute("INSERT OR IGNORE INTO usuarios (token, nombre) VALUES ('INVALID', 'No Autorizado')")
    conn.commit()
    conn.close()

init_db()

@app.route('/check')
def check():
    token = request.args.get('token')
    if not token:
        return jsonify({"autorizado": False})
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT nombre FROM usuarios WHERE token = ?", (token,))
    row = c.fetchone()
    conn.close()
    if row:
        return jsonify({"autorizado": True, "nombre": row[0]})
    else:
        return jsonify({"autorizado": False})

@app.route('/log', methods=['POST'])
def log_event():
    data = request.get_json()
    token = data.get('token')
    timestamp = data.get('timestamp')
    resultado = data.get('resultado')
    if not all([token, timestamp, resultado]):
        return jsonify({"error": "Datos faltantes"}), 400
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT INTO logs (token, timestamp, resultado) VALUES (?, ?, ?)", (token, timestamp, resultado))
    conn.commit()
    conn.close()
    return jsonify({"status": "registrado"})

@app.route('/usuarios', methods=['GET'])
def get_usuarios():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT token, nombre FROM usuarios")
    rows = c.fetchall()
    conn.close()
    users = [{"token": r[0], "nombre": r[1]} for r in rows]
    return jsonify(users)

@app.route('/usuarios', methods=['POST'])
def add_usuario():
    data = request.get_json()
    token = data.get('token')
    nombre = data.get('nombre')
    if not all([token, nombre]):
        return jsonify({"error": "Datos faltantes"}), 400
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO usuarios (token, nombre) VALUES (?, ?)", (token, nombre))
        conn.commit()
        return jsonify({"status": "agregado"})
    except sqlite3.IntegrityError:
        return jsonify({"error": "Token ya existe"}), 400
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)