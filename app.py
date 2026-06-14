from flask import Flask, render_template
import socket
import re

app = Flask(__name__)

HOST = "10.190.224.152"  # IP del servidor del sensor
PORT = 12345              # Puerto del servidor
TIMEOUT = 2               # Tiempo máximo de espera en segundos

def leer_sensor():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(TIMEOUT)
            s.connect((HOST, PORT))

            data = s.recv(1024).decode().strip()
            print("RECIBIDO:", data)

            # Formato esperado: X:12.5,Y:-3.2
            match = re.search(
                r"X:\s*(-?\d+(?:\.\d+)?),\s*Y:\s*(-?\d+(?:\.\d+)?)",
                data
            )

            if not match:
                raise ValueError("Formato incorrecto. Se esperaba: X:valor,Y:valor")

            ejeX = float(match.group(1))
            ejeY = float(match.group(2))

            return ejeX, ejeY

    except Exception as e:
        print("ERROR:", e)
        return 0, 0  # Valores por defecto en caso de error

def obtener_cuadrante(x, y):
    if x > 0 and y > 0:
        return "Q1"
    elif x < 0 and y > 0:
        return "Q2"
    elif x < 0 and y < 0:
        return "Q3"
    elif x > 0 and y < 0:
        return "Q4"
    else:
        return "Eje"

@app.route("/")
def index():
    ejeX, ejeY = leer_sensor()
    cuadrante = obtener_cuadrante(ejeX, ejeY)

    return render_template(
        "index.html",
        ejeX=ejeX,
        ejeY=ejeY,
        cuadrante=cuadrante
    )

@app.route("/devices")
def devices():
    return render_template("device.html")

@app.route("/devices/defy")
def defy():
    return render_template("devices/defy.html")

@app.route("/devices/edge")
def edge():
    return render_template("devices/edge.html")

@app.route("/devices/lenovo-k-series")
def lenovo_k_series():
    return render_template("devices/lenovo-k-series.html")

@app.route("/devices/moto-e")
def moto_e():
    return render_template("devices/moto-e.html")

@app.route("/devices/moto-g")
def moto_g():
    return render_template("devices/moto-g.html")

@app.route("/devices/moto-p")
def moto_p():
    return render_template("devices/moto-p.html")

@app.route("/devices/moto-s")
def moto_s():
    return render_template("devices/moto-s.html")

@app.route("/devices/moto-x")
def moto_x():
    return render_template("devices/moto-x.html")

@app.route("/devices/moto-z")
def moto_z():
    return render_template("devices/moto-z.html")

@app.route("/devices/one")
def one():
    return render_template("devices/one.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
