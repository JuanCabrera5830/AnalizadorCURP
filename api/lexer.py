import ply.lex as lex

tokens = (
    'NOMBRE', 'APELLIDO1', 'APELLIDO2',
    'FECHA', 'SEXO', 'ESTADO'
)

t_ignore = ' \t'

def t_NOMBRE(t):
    r'NOMBRE=[A-ZÁÉÍÓÚÑ ]+'
    t.value = t.value.split('=', 1)[1].strip()
    return t

def t_APELLIDO1(t):
    r'APELLIDO1=[A-ZÁÉÍÓÚÑ ]+'
    t.value = t.value.split('=', 1)[1].strip()
    return t

def t_APELLIDO2(t):
    r'APELLIDO2=[A-ZÁÉÍÓÚÑ ]+'
    t.value = t.value.split('=', 1)[1].strip()
    return t

def t_FECHA(t):
    r'FECHA=\d{4}-\d{2}-\d{2}'
    t.value = t.value.split('=')[1]
    return t

def t_SEXO(t):
    r'SEXO=[HM]'
    t.value = t.value.split('=')[1]
    return t

def t_ESTADO(t):
    r'ESTADO=[A-ZÁÉÍÓÚÑ ]+'
    t.value = t.value.split('=', 1)[1].strip()
    return t

def t_newline(t):
    r'\n+'
    pass

def t_error(t):
    raise SyntaxError(f"Token inválido: {t.value}")

lexer = lex.lex()