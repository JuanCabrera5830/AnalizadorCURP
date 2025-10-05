import ply.yacc as yacc
from lexer import tokens

estados_clave = {
    "AGUASCALIENTES": "AS", "BAJA CALIFORNIA": "BC", "BAJA CALIFORNIA SUR": "BS",
    "CAMPECHE": "CC", "COAHUILA": "CL", "COLIMA": "CM", "CHIAPAS": "CS",
    "CHIHUAHUA": "CH", "CIUDAD DE MEXICO": "DF", "DURANGO": "DG", "GUANAJUATO": "GT",
    "GUERRERO": "GR", "HIDALGO": "HG", "JALISCO": "JC", "ESTADO DE MEXICO": "MC",
    "MICHOACAN": "MN", "MORELOS": "MS", "NAYARIT": "NT", "NUEVO LEON": "NL",
    "OAXACA": "OC", "PUEBLA": "PL", "QUERETARO": "QT", "QUINTANA ROO": "QR",
    "SAN LUIS POTOSI": "SP", "SINALOA": "SL", "SONORA": "SR", "TABASCO": "TC",
    "TAMAULIPAS": "TS", "TLAXCALA": "TL", "VERACRUZ": "VZ", "YUCATAN": "YN",
    "ZACATECAS": "ZS", "NACIDO EN EL EXTRANJERO": "NE"
}

def p_data(p):
    'data : NOMBRE APELLIDO1 APELLIDO2 FECHA SEXO ESTADO'
    p[0] = generar_curp(p[2], p[3], p[1], p[4], p[5], p[6])

def p_error(p):
    raise SyntaxError("Error de sintaxis en los datos")

def generar_curp(ap1, ap2, nombre, fecha, sexo, estado):
    curp = ap1[0]
    vocales = 'AEIOU'
    interna = next((c for c in ap1[1:] if c in vocales), 'X')
    curp += interna
    curp += ap2[0] if ap2 else 'X'
    curp += nombre[0]

    year, month, day = fecha.split('-')
    curp += year[2:] + month + day

    curp += sexo

    clave_estado = estados_clave.get(estado.upper(), "NE")
    curp += clave_estado

    def consonante_interna(word):
        return next((c for c in word[1:] if c not in 'AEIOU'), 'X')

    curp += consonante_interna(ap1)
    curp += consonante_interna(ap2)
    curp += consonante_interna(nombre)

    curp += 'A0' if int(year) > 2000 else '00'

    return curp.upper()

parser = yacc.yacc()

def parse_input(input_text):
    try:
        return parser.parse(input_text.upper())
    except Exception as e:
        return f"Error: {e}"