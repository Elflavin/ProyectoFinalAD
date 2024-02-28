# Podemos cambiar algunas cosas en esta clase para admitir pruebas directas relacionadas con la bd

def validarEntero(vacio, mensaje, intentos=5):
    for _ in range(intentos):
        try:
            valor_str = input(mensaje)
            if vacio and valor_str.strip() == "":
                return None
            else:
                valor = int(valor_str)
                return valor
        except ValueError:
            print("Error: Debe ingresar un número entero.")
    print("Demasiados intentos fallidos. Abortando operación.")
    return None


def validarCadena(vacio, mensaje, intentos=5):
    for _ in range(intentos):
        valor = input(mensaje)
        if valor.replace(" ", "").isalpha():
            return valor
        elif (vacio and valor == ""):
            return None
        else:
            print("debe ingresar solo letras")
    print("Demasiados intentos fallidos. Abortando operación.")

def validarDni(vacio, mensaje, intentos):
    for _ in range(intentos):
        valor = input(mensaje).strip()
        if len(valor) == 9 and valor[:-1].isdigit() and valor[-1].isalpha():
            return valor.upper()  # Convertir la letra a mayuscula
        elif vacio and valor == "":
            return None
        else:
            print("Debe ingresar un DNI valido (XXXXXXXXL).")
    print("Demasiados intentos fallidos. Abortando operacion.")
