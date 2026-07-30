import ast
import os
import sqlite3
from flask import Flask, request

app = Flask(__name__)

# ✔️ SEGURIDAD: Evitar credenciales hardcodeadas (se lee de variable de entorno)
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")


@app.route("/buscar")
def buscar():
    termino = request.args.get("q", "")
    conexion = sqlite3.connect("datos.db")

    # ✔️ SEGURIDAD: Consulta parametrizada para prevenir inyección SQL (SQLi)
    consulta = "SELECT * FROM productos WHERE nombre = ?"
    resultado = conexion.execute(consulta, (termino,))

    datos = resultado.fetchall()
    conexion.close()
    return str(datos)


@app.route("/calcular")
def calcular():
    expresion = request.args.get("expr", "")
    try:
        # ✔️ SEGURIDAD: ast.literal_eval previene la ejecución remota de código (RCE)
        resultado = ast.literal_eval(expresion)
    except (ValueError, SyntaxError):
        resultado = "Expresión no válida"

    return str(resultado)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)