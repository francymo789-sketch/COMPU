import json
import os


ARCHIVO_MAQUINARIA = "maquinaria.json"


def cargar_maquinaria():
    """Carga la lista de maquinaria desde un archivo JSON."""
    if not os.path.exists(ARCHIVO_MAQUINARIA):
        return []

    try:
        with open(ARCHIVO_MAQUINARIA, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

            if isinstance(datos, list):
                return datos

            return []

    except json.JSONDecodeError:
        return []


def guardar_maquinaria(lista_maquinaria):
    """Guarda la lista de maquinaria en un archivo JSON."""
    with open(ARCHIVO_MAQUINARIA, "w", encoding="utf-8") as archivo:
        json.dump(lista_maquinaria, archivo, indent=4, ensure_ascii=False)


def validar_texto(valor, nombre_campo):
    """Valida que un texto no esté vacío."""
    if not isinstance(valor, str) or valor.strip() == "":
        return False, f"El campo {nombre_campo} no puede estar vacío."

    return True, ""


def validar_entero_positivo(valor, nombre_campo):
    """Valida que un valor sea un número entero positivo."""
    try:
        numero = int(valor)

        if numero < 0:
            return False, f"El campo {nombre_campo} no puede ser negativo."

        return True, ""

    except ValueError:
        return False, f"El campo {nombre_campo} debe ser un número entero."


def existe_codigo(lista_maquinaria, codigo):
    """Verifica si ya existe una maquinaria con el mismo código."""
    for maquinaria in lista_maquinaria:
        if maquinaria["codigo"] == codigo:
            return True

    return False


def crear_maquinaria(codigo, nombre, tipo, marca, modelo, anio, horas_uso, estado):
    """Crea un diccionario con los datos de una maquinaria validada."""
    maquinaria = {
        "codigo": codigo.strip(),
        "nombre": nombre.strip(),
        "tipo": tipo.strip(),
        "marca": marca.strip(),
        "modelo": modelo.strip(),
        "anio": int(anio),
        "horas_uso": int(horas_uso),
        "estado": estado.strip()
    }

    return maquinaria


def registrar_maquinaria(lista_maquinaria, codigo, nombre, tipo, marca, modelo, anio, horas_uso, estado):
    """Registra una nueva maquinaria en la lista."""
    campos_texto = {
        "código": codigo,
        "nombre": nombre,
        "tipo": tipo,
        "marca": marca,
        "modelo": modelo,
        "estado": estado
    }

    for nombre_campo, valor in campos_texto.items():
        es_valido, mensaje = validar_texto(valor, nombre_campo)
        if not es_valido:
            return False, mensaje

    es_valido, mensaje = validar_entero_positivo(anio, "año")
    if not es_valido:
        return False, mensaje

    es_valido, mensaje = validar_entero_positivo(horas_uso, "horas de uso")
    if not es_valido:
        return False, mensaje

    if existe_codigo(lista_maquinaria, codigo.strip()):
        return False, "Ya existe una maquinaria registrada con ese código."

    nueva_maquinaria = crear_maquinaria(
        codigo,
        nombre,
        tipo,
        marca,
        modelo,
        anio,
        horas_uso,
        estado
    )

    lista_maquinaria.append(nueva_maquinaria)
    guardar_maquinaria(lista_maquinaria)

    return True, "Maquinaria registrada correctamente."


def listar_maquinaria(lista_maquinaria):
    """Devuelve la lista completa de maquinaria registrada."""
    return lista_maquinaria


def buscar_maquinaria_por_codigo(lista_maquinaria, codigo):
    """Busca una maquinaria usando su código."""
    for maquinaria in lista_maquinaria:
        if maquinaria["codigo"] == codigo.strip():
            return maquinaria

    return None

