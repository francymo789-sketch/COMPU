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
import json
import os
from datetime import datetime


ARCHIVO_MANTENIMIENTOS = "mantenimientos.json"

TIPOS_MANTENIMIENTO = [
    "Preventivo",
    "Correctivo",
    "Predictivo"
]

ESTADOS_MANTENIMIENTO = [
    "Programado",
    "En proceso",
    "Finalizado",
    "Cancelado"
]


def cargar_mantenimientos():
    """Carga la lista de mantenimientos desde un archivo JSON."""
    if not os.path.exists(ARCHIVO_MANTENIMIENTOS):
        return []

    try:
        with open(ARCHIVO_MANTENIMIENTOS, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

            if isinstance(datos, list):
                return datos

            return []

    except json.JSONDecodeError:
        return []


def guardar_mantenimientos(lista_mantenimientos):
    """Guarda la lista de mantenimientos en un archivo JSON."""
    with open(ARCHIVO_MANTENIMIENTOS, "w", encoding="utf-8") as archivo:
        json.dump(lista_mantenimientos, archivo, indent=4, ensure_ascii=False)


def validar_texto_mantenimiento(valor, nombre_campo):
    """Valida que un campo de texto obligatorio no esté vacío."""
    if not isinstance(valor, str) or valor.strip() == "":
        return False, f"El campo {nombre_campo} no puede estar vacío."

    return True, ""


def validar_fecha(fecha, nombre_campo):
    """Valida que una fecha tenga el formato AAAA-MM-DD."""
    es_valido, mensaje = validar_texto_mantenimiento(fecha, nombre_campo)

    if not es_valido:
        return False, mensaje

    try:
        datetime.strptime(fecha.strip(), "%Y-%m-%d")
        return True, ""

    except ValueError:
        return False, f"El campo {nombre_campo} debe tener el formato AAAA-MM-DD."


def validar_fecha_opcional(fecha, nombre_campo):
    """Valida una fecha opcional si fue ingresada."""
    if fecha is None or fecha.strip() == "":
        return True, ""

    return validar_fecha(fecha, nombre_campo)


def validar_costo_mantenimiento(costo):
    """Valida que el costo sea numérico y no negativo."""
    try:
        costo_convertido = float(costo)

        if costo_convertido < 0:
            return False, "El costo del mantenimiento no puede ser negativo."

        return True, ""

    except ValueError:
        return False, "El costo del mantenimiento debe ser numérico."


def validar_tipo_mantenimiento(tipo_mantenimiento):
    """Valida que el tipo de mantenimiento esté permitido."""
    if tipo_mantenimiento not in TIPOS_MANTENIMIENTO:
        return False, "El tipo de mantenimiento no es válido."

    return True, ""


def validar_estado_mantenimiento(estado):
    """Valida que el estado del mantenimiento esté permitido."""
    if estado not in ESTADOS_MANTENIMIENTO:
        return False, "El estado del mantenimiento no es válido."

    return True, ""


def existe_codigo_mantenimiento(lista_mantenimientos, codigo_mantenimiento):
    """Verifica si ya existe un mantenimiento con el mismo código."""
    for mantenimiento in lista_mantenimientos:
        if mantenimiento["codigo_mantenimiento"] == codigo_mantenimiento.strip():
            return True

    return False


def existe_maquinaria(lista_maquinaria, codigo_maquinaria):
    """Verifica si existe una maquinaria registrada con el código indicado."""
    for maquinaria in lista_maquinaria:
        if maquinaria["codigo"] == codigo_maquinaria.strip():
            return True

    return False


def crear_mantenimiento(
    codigo_mantenimiento,
    codigo_maquinaria,
    tipo_mantenimiento,
    fecha_programada,
    fecha_realizada,
    descripcion,
    responsable,
    costo,
    estado
):
    """Crea un diccionario con los datos de un mantenimiento."""
    mantenimiento = {
        "codigo_mantenimiento": codigo_mantenimiento.strip(),
        "codigo_maquinaria": codigo_maquinaria.strip(),
        "tipo_mantenimiento": tipo_mantenimiento.strip(),
        "fecha_programada": fecha_programada.strip(),
        "fecha_realizada": fecha_realizada.strip(),
        "descripcion": descripcion.strip(),
        "responsable": responsable.strip(),
        "costo": float(costo),
        "estado": estado.strip()
    }

    return mantenimiento


def validar_datos_mantenimiento(
    lista_maquinaria,
    codigo_mantenimiento,
    codigo_maquinaria,
    tipo_mantenimiento,
    fecha_programada,
    fecha_realizada,
    descripcion,
    responsable,
    costo,
    estado
):
    """Valida todos los datos antes de registrar un mantenimiento."""
    campos_texto = {
        "código de mantenimiento": codigo_mantenimiento,
        "código de maquinaria": codigo_maquinaria,
        "descripción": descripcion,
        "responsable": responsable
    }

    for nombre_campo, valor in campos_texto.items():
        es_valido, mensaje = validar_texto_mantenimiento(valor, nombre_campo)

        if not es_valido:
            return False, mensaje

    if not existe_maquinaria(lista_maquinaria, codigo_maquinaria):
        return False, "No existe una maquinaria registrada con ese código."

    es_valido, mensaje = validar_tipo_mantenimiento(tipo_mantenimiento.strip())

    if not es_valido:
        return False, mensaje

    es_valido, mensaje = validar_fecha(fecha_programada, "fecha programada")

    if not es_valido:
        return False, mensaje

    es_valido, mensaje = validar_fecha_opcional(fecha_realizada, "fecha realizada")

    if not es_valido:
        return False, mensaje

    es_valido, mensaje = validar_costo_mantenimiento(costo)

    if not es_valido:
        return False, mensaje

    es_valido, mensaje = validar_estado_mantenimiento(estado.strip())

    if not es_valido:
        return False, mensaje

    return True, ""


def registrar_mantenimiento(
    lista_mantenimientos,
    lista_maquinaria,
    codigo_mantenimiento,
    codigo_maquinaria,
    tipo_mantenimiento,
    fecha_programada,
    fecha_realizada,
    descripcion,
    responsable,
    costo,
    estado
):
    """Registra un mantenimiento asociado a una maquinaria existente."""
    es_valido, mensaje = validar_datos_mantenimiento(
        lista_maquinaria,
        codigo_mantenimiento,
        codigo_maquinaria,
        tipo_mantenimiento,
        fecha_programada,
        fecha_realizada,
        descripcion,
        responsable,
        costo,
        estado
    )

    if not es_valido:
        return False, mensaje

    if existe_codigo_mantenimiento(lista_mantenimientos, codigo_mantenimiento):
        return False, "Ya existe un mantenimiento registrado con ese código."

    nuevo_mantenimiento = crear_mantenimiento(
        codigo_mantenimiento,
        codigo_maquinaria,
        tipo_mantenimiento,
        fecha_programada,
        fecha_realizada,
        descripcion,
        responsable,
        costo,
        estado
    )

    lista_mantenimientos.append(nuevo_mantenimiento)
    guardar_mantenimientos(lista_mantenimientos)

    return True, "Mantenimiento registrado correctamente."


def listar_mantenimientos(lista_mantenimientos):
    """Devuelve la lista completa de mantenimientos registrados."""
    return lista_mantenimientos


def buscar_mantenimiento_por_codigo(lista_mantenimientos, codigo_mantenimiento):
    """Busca un mantenimiento por su código."""
    for mantenimiento in lista_mantenimientos:
        if mantenimiento["codigo_mantenimiento"] == codigo_mantenimiento.strip():
            return mantenimiento

    return None


def listar_mantenimientos_por_maquinaria(lista_mantenimientos, codigo_maquinaria):
    """Lista los mantenimientos asociados a una maquinaria."""
    mantenimientos_encontrados = []

    for mantenimiento in lista_mantenimientos:
        if mantenimiento["codigo_maquinaria"] == codigo_maquinaria.strip():
            mantenimientos_encontrados.append(mantenimiento)

    return mantenimientos_encontrados
