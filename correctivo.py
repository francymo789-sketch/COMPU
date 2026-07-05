import json
import os
from datetime import datetime


ARCHIVO_CORRECTIVOS = "correctivos.json"

PRIORIDADES_CORRECTIVO = [
    "Baja",
    "Media",
    "Alta",
    "Crítica"
]

ESTADOS_CORRECTIVO = [
    "Reportado",
    "En revisión",
    "En reparación",
    "Resuelto",
    "Cancelado"
]


def cargar_correctivos():
    """Carga la lista de fallas correctivas desde un archivo JSON."""
    if not os.path.exists(ARCHIVO_CORRECTIVOS):
        return []

    try:
        with open(ARCHIVO_CORRECTIVOS, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

            if isinstance(datos, list):
                return datos

            return []

    except json.JSONDecodeError:
        return []


def guardar_correctivos(lista_correctivos):
    """Guarda la lista de fallas correctivas en un archivo JSON."""
    with open(ARCHIVO_CORRECTIVOS, "w", encoding="utf-8") as archivo:
        json.dump(lista_correctivos, archivo, indent=4, ensure_ascii=False)


def validar_texto_correctivo(valor, nombre_campo):
    """Valida que un campo obligatorio no esté vacío."""
    if not isinstance(valor, str):
        return False, f"El campo {nombre_campo} debe ser texto."

    if valor.strip() == "":
        return False, f"El campo {nombre_campo} no puede estar vacío."

    return True, ""


def validar_fecha_correctivo(fecha, nombre_campo):
    """Valida una fecha con formato AAAA-MM-DD."""
    es_valido, mensaje = validar_texto_correctivo(fecha, nombre_campo)

    if not es_valido:
        return False, mensaje

    try:
        datetime.strptime(fecha.strip(), "%Y-%m-%d")
        return True, ""

    except ValueError:
        return False, f"El campo {nombre_campo} debe tener el formato AAAA-MM-DD."


def validar_fecha_opcional_correctivo(fecha, nombre_campo):
    """Valida una fecha opcional si fue ingresada."""
    if fecha is None:
        return True, ""

    if not isinstance(fecha, str):
        return False, f"El campo {nombre_campo} debe ser texto."

    if fecha.strip() == "":
        return True, ""

    return validar_fecha_correctivo(fecha, nombre_campo)


def validar_prioridad_correctivo(prioridad):
    """Valida que la prioridad del correctivo esté permitida."""
    es_valido, mensaje = validar_texto_correctivo(prioridad, "prioridad")

    if not es_valido:
        return False, mensaje

    if prioridad.strip() not in PRIORIDADES_CORRECTIVO:
        return False, "La prioridad del correctivo no es válida."

    return True, ""


def validar_estado_correctivo(estado):
    """Valida que el estado del correctivo esté permitido."""
    es_valido, mensaje = validar_texto_correctivo(estado, "estado")

    if not es_valido:
        return False, mensaje

    if estado.strip() not in ESTADOS_CORRECTIVO:
        return False, "El estado del correctivo no es válido."

    return True, ""


def existe_equipo(lista_equipos, codigo_equipo):
    """Verifica si existe un equipo registrado."""
    for equipo in lista_equipos:
        if equipo["codigo"].lower() == codigo_equipo.strip().lower():
            return True

    return False


def existe_codigo_correctivo(lista_correctivos, codigo_correctivo):
    """Verifica si ya existe un correctivo con el mismo código."""
    for correctivo in lista_correctivos:
        if correctivo["codigo_correctivo"].lower() == codigo_correctivo.strip().lower():
            return True

    return False


def crear_correctivo(
    codigo_correctivo,
    codigo_equipo,
    fecha_reporte,
    descripcion,
    prioridad,
    responsable,
    estado,
    fecha_solucion
):
    """Crea un diccionario con los datos del correctivo."""
    correctivo = {
        "codigo_correctivo": codigo_correctivo.strip().upper(),
        "codigo_equipo": codigo_equipo.strip().upper(),
        "fecha_reporte": fecha_reporte.strip(),
        "descripcion": descripcion.strip(),
        "prioridad": prioridad.strip(),
        "responsable": responsable.strip(),
        "estado": estado.strip(),
        "fecha_solucion": fecha_solucion.strip()
    }

    return correctivo


def validar_datos_correctivo(
    lista_equipos,
    codigo_correctivo,
    codigo_equipo,
    fecha_reporte,
    descripcion,
    prioridad,
    responsable,
    estado,
    fecha_solucion
):
    """Valida todos los datos antes de registrar un correctivo."""
    campos_texto = {
        "código correctivo": codigo_correctivo,
        "código de equipo": codigo_equipo,
        "descripción": descripcion,
        "responsable": responsable
    }

    for nombre_campo, valor in campos_texto.items():
        es_valido, mensaje = validar_texto_correctivo(valor, nombre_campo)

        if not es_valido:
            return False, mensaje

    if not existe_equipo(lista_equipos, codigo_equipo):
        return False, "No existe un equipo registrado con ese código."

    es_valido, mensaje = validar_fecha_correctivo(fecha_reporte, "fecha de reporte")

    if not es_valido:
        return False, mensaje

    es_valido, mensaje = validar_prioridad_correctivo(prioridad)

    if not es_valido:
        return False, mensaje

    es_valido, mensaje = validar_estado_correctivo(estado)

    if not es_valido:
        return False, mensaje

    es_valido, mensaje = validar_fecha_opcional_correctivo(
        fecha_solucion,
        "fecha de solución"
    )

    if not es_valido:
        return False, mensaje

    return True, ""


def registrar_correctivo(
    lista_correctivos,
    lista_equipos,
    codigo_correctivo,
    codigo_equipo,
    fecha_reporte,
    descripcion,
    prioridad,
    responsable,
    estado,
    fecha_solucion
):
    """Registra una falla o ticket correctivo asociado a un equipo existente."""
    es_valido, mensaje = validar_datos_correctivo(
        lista_equipos,
        codigo_correctivo,
        codigo_equipo,
        fecha_reporte,
        descripcion,
        prioridad,
        responsable,
        estado,
        fecha_solucion
    )

    if not es_valido:
        return False, mensaje

    if existe_codigo_correctivo(lista_correctivos, codigo_correctivo):
        return False, "Ya existe un correctivo registrado con ese código."

    nuevo_correctivo = crear_correctivo(
        codigo_correctivo,
        codigo_equipo,
        fecha_reporte,
        descripcion,
        prioridad,
        responsable,
        estado,
        fecha_solucion
    )

    lista_correctivos.append(nuevo_correctivo)
    guardar_correctivos(lista_correctivos)

    return True, "Correctivo registrado correctamente."


def listar_correctivos(lista_correctivos):
    """Devuelve la lista completa de correctivos registrados."""
    return lista_correctivos


def buscar_correctivo_por_codigo(lista_correctivos, codigo_correctivo):
    """Busca un correctivo por su código."""
    for correctivo in lista_correctivos:
        if correctivo["codigo_correctivo"].lower() == codigo_correctivo.strip().lower():
            return correctivo

    return None


def listar_correctivos_por_equipo(lista_correctivos, codigo_equipo):
    """Lista correctivos asociados a un equipo."""
    correctivos_encontrados = []

    for correctivo in lista_correctivos:
        if correctivo["codigo_equipo"].lower() == codigo_equipo.strip().lower():
            correctivos_encontrados.append(correctivo)

    return correctivos_encontrados


def listar_correctivos_pendientes(lista_correctivos):
    """Lista correctivos que aún no están resueltos."""
    correctivos_pendientes = []

    for correctivo in lista_correctivos:
        if correctivo["estado"] not in ["Resuelto", "Cancelado"]:
            correctivos_pendientes.append(correctivo)

    return correctivos_pendientes


def cambiar_estado_correctivo(lista_correctivos, codigo_correctivo, nuevo_estado):
    """Cambia el estado de un correctivo registrado."""
    es_valido, mensaje = validar_estado_correctivo(nuevo_estado)

    if not es_valido:
        return False, mensaje

    correctivo = buscar_correctivo_por_codigo(lista_correctivos, codigo_correctivo)

    if correctivo is None:
        return False, "No existe un correctivo registrado con ese código."

    correctivo["estado"] = nuevo_estado.strip()
    guardar_correctivos(lista_correctivos)

    return True, "Estado del correctivo actualizado correctamente."
