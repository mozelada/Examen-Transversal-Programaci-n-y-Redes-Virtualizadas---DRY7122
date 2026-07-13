import sqlite3
import hashlib
from flask import Flask, jsonify, request

app = Flask(__name__)
DB_NAME = "usuarios_examen.db"

def inicializar_base_de_datos():
    """Crea la tabla de usuarios si no existe e inserta a los integrantes."""
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    
    # Crear tabla con id, usuario y la contraseña almacenada en hash
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        )
    ''')
    
    # Lista de los integrantes del grupo (modifica con tus nombres reales)
    # Definimos contraseñas iniciales a elección para la demostración
    integrantes = {
        "Montserrat_Zelada": "claveSegura123",
    }
    
    for usuario, clave_plana in integrantes.items():
        # Aplicamos hash SHA-256 a la contraseña plana
        hash_objeto = hashlib.sha256(clave_plana.encode('utf-8'))
        clave_con_hash = hash_objeto.hexdigest()
        
        try:
            cursor.execute(
                "INSERT INTO usuarios (nombre, password_hash) VALUES (?, ?)", 
                (usuario, clave_con_hash)
            )
            print(f"Montse '{usuario}' registrado exitosamente con hash.")
        except sqlite3.IntegrityError:
            # Si el usuario ya existe en ejecuciones anteriores, ignoramos el error
            pass
            
    conexion.commit()
    conexion.close()

@app.route('/')
def home():
    return jsonify({
        "mensaje": "Servidor activo para el Examen Transversal DRY7122",
        "status": "online"
    })

@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    """Ruta API complementaria para listar los hashes desde la web."""
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    cursor.execute("SELECT nombre, password_hash FROM usuarios")
    filas = cursor.fetchall()
    conexion.close()
    
    resultado = [{"usuario": f[0], "password_hash": f[1]} for f in filas]
    return jsonify(resultado)

if __name__ == "__main__":
    # Inicializa la base de datos e inserta los datos antes de encender la web
    inicializar_base_de_datos()
    
    print("\nLanzando el servidor web en el puerto 5800 solicitado...")
    # Levantamos en el puerto 5800 estipulado en los requerimientos
    app.run(host="0.0.0.0", port=5800, debug=True)
    