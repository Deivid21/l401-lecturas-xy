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

@app.route('/')
def index():
    ejeY, ejeX = leer_sensor() #órden ejes.
    return render_template(
        'index.html',
        ejeX=ejeX,
        ejeY=ejeY
    )
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
