# Podemos cambiar algunas cosas en esta clase para admitir pruebas directas relacionadas con la bd

# Vacio esta para cuando quieras modificar, si no es asi pasa por parametro False.
# Valor es el dato que debemos manejar
# En intentos pone el numero de intentos que quieras que tenga el usuario

def validarEntero(vacio, valor, intentos): 
    for _ in range(intentos):
        try:
            if vacio and valor.strip() == "":
                return None
            else:
                valor_int = int(valor)
                return valor
        except ValueError:
            print("Error: Debe ingresar un número entero.")
    print("Demasiados intentos fallidos. Abortando operación.")
    return None


def validarCadena(vacio, valor, intentos):
    for _ in range(intentos):
        if valor.replace(" ", "").isalpha():
            return valor
        elif (vacio and valor == ""):
            return None
        else:
            print("debe ingresar solo letras")
    print("Demasiados intentos fallidos. Abortando operación.")

def validarDni(vacio, valor, intentos):
    for _ in range(intentos):
        if len(valor) == 9 and valor[:-1].isdigit() and valor[-1].isalpha():
            return valor.upper()  # Convertir la letra a mayuscula
        elif vacio and valor == "":
            return None
        else:
            print("Debe ingresar un DNI valido (XXXXXXXXL).")
    print("Demasiados intentos fallidos. Abortando operacion.")
