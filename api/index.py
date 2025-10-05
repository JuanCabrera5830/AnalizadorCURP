from flask import Flask, request, jsonify
from parser import parse_input
from datetime import datetime
import re
import sys

app = Flask(__name__)

def es_nombre_posible(valor):
    if len(valor) < 3:
        return False
    valor = valor.upper()
    if not any(c in "AEIOUÁÉÍÓÚ" for c in valor):
        return False
    if re.search(r'[BCDFGHJKLMNÑPQRSTVWXYZ]{4,}', valor):
        return False
    return True

def validar_entrada(nombre, apellido1, apellido2, fecha, sexo, estado):
    errores = []
    caracteres_validos = "ABCDEFGHIJKLMNOPQRSTUVWXYZÁÉÍÓÚÑ "
    campos_obligatorios = {'Nombre': nombre, 'Apellido paterno': apellido1}

    for campo, valor in campos_obligatorios.items():
        if not valor or len(valor.strip()) < 4:
            errores.append(f"{campo} no puede estar vacío o incompleto (mínimo 4 letras).")
        elif not all(c in caracteres_validos for c in valor.upper()):
            errores.append(f"{campo} contiene caracteres inválidos.")
        elif not es_nombre_posible(valor):
            errores.append(f"{campo} no parece un nombre/apellido real.")

    if apellido2:
        if len(apellido2.strip()) < 4:
            errores.append("Apellido materno debe tener al menos 4 letras si se proporciona.")
        elif not all(c in caracteres_validos for c in apellido2.upper()):
            errores.append("Apellido materno contiene caracteres inválidos.")
        elif not es_nombre_posible(apellido2):
            errores.append("Apellido materno no parece un apellido real.")

    try:
        datetime.strptime(fecha, "%Y-%m-%d")
    except ValueError:
        errores.append("Fecha de nacimiento inválida. Debe tener formato YYYY-MM-DD.")

    if sexo not in ['H', 'M']:
        errores.append("Sexo inválido. Debe ser 'H' o 'M'.")

    estados_validos = [
        "AGUASCALIENTES", "BAJA CALIFORNIA", "BAJA CALIFORNIA SUR", "CAMPECHE",
        "COAHUILA", "COLIMA", "CHIAPAS", "CHIHUAHUA", "CIUDAD DE MEXICO",
        "DURANGO", "GUANAJUATO", "GUERRERO", "HIDALGO", "JALISCO",
        "ESTADO DE MEXICO", "MICHOACAN", "MORELOS", "NAYARIT", "NUEVO LEON",
        "OAXACA", "PUEBLA", "QUERETARO", "QUINTANA ROO", "SAN LUIS POTOSI",
        "SINALOA", "SONORA", "TABASCO", "TAMAULIPAS", "TLAXCALA", "VERACRUZ",
        "YUCATAN", "ZACATECAS", "NACIDO EN EL EXTRANJERO"
    ]
    if estado.upper() not in estados_validos:
        errores.append("Estado inválido. Selecciona uno válido.")

    return errores

@app.route('/', methods=['POST'])
def handler():
    data = request.get_json()
    # Debug logs para revisar en los logs de Vercel
    print("DEBUG: datos recibidos:", data, file=sys.stderr)

    nombre = data.get('nombre', '')
    apellido1 = data.get('apellido1', '')
    apellido2 = data.get('apellido2', '')
    fecha = data.get('fecha', '')
    sexo = data.get('sexo', '')
    estado = data.get('estado', '')

    errores = validar_entrada(nombre, apellido1, apellido2, fecha, sexo, estado)
    print("DEBUG: errores de validación:", errores, file=sys.stderr)
    if errores:
        return jsonify({"errores": errores}), 400

    datos_para_parse = f"""
    NOMBRE={nombre}
    APELLIDO1={apellido1}
    APELLIDO2={apellido2}
    FECHA={fecha}
    SEXO={sexo}
    ESTADO={estado}
    """.strip().upper()
    print("DEBUG: datos_para_parse:", datos_para_parse, file=sys.stderr)

    curp = parse_input(datos_para_parse)
    print("DEBUG: resultado parse_input:", curp, file=sys.stderr)

    if "Error" in str(curp):
        return jsonify({"errores": [str(curp)]}), 400

    return jsonify({"curp": curp})

handler = app