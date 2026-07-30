import ast
import os
import sqlite3
from flask import Flask, request
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

# Configurar una Secret Key para generar y validar los tokens CSRF
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'clave-secreta-para-dev')

# Inicializar la protección CSRF (resuelve la regla SAST python:S4502 / CSRF)
csrf = CSRFProtect(app)

# SEGURIDAD: Evitar credenciales hardcodeadas (se lee de variable de entorno)
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")


@app.route("/buscar")
def buscar():
    termino = request.args.get("q", "")
    conexion = sqlite3.connect("datos.db")

    # SEGURIDAD: Consulta parametrizada para prevenir inyección SQL (SQLi)
    consulta = "SELECT * FROM productos WHERE nombre = ?"
    resultado = conexion.execute(consulta, (termino,))

    datos = resultado.fetchall()
    conexion.close()
    return str(datos)


@app.route("/calcular")
def calcular():
    expresion = request.args.get("expr", "")
    try:
        # SEGURIDAD: ast.literal_eval previene la ejecución remota de código (RCE)
        resultado = ast.literal_eval(expresion)
    except (ValueError, SyntaxError):
        resultado = "Expresión no válida"

    return str(resultado)


if __name__ == "__main__":
    # SEGURIDAD: Escuchar solo en localhost (127.0.0.1) en lugar de todas las interfaces (0.0.0.0)
    app.run(host="127.0.0.1", port=8080)