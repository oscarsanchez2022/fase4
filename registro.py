# registro.py
# Configura el archivo de logs donde se guardan los eventos y los errores.

import logging  # modulo de Python para registrar mensajes (logs)
import os  # modulo para trabajar con rutas y carpetas

# La carpeta de logs se crea junto a este archivo
CARPETA_LOGS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")  # ruta de la carpeta
ARCHIVO_LOG = os.path.join(CARPETA_LOGS, "software_fj.log")  # ruta del archivo de logs

def crear_logger():  # arma el logger que usara todo el sistema
    """Devuelve el logger del sistema, listo para escribir en el archivo."""
    os.makedirs(CARPETA_LOGS, exist_ok=True)  # crea la carpeta si no existe

    logger = logging.getLogger("software_fj")  # pide un logger con nombre propio
    logger.setLevel(logging.INFO)  # guarda mensajes desde nivel INFO hacia arriba

    # Si ya tiene handlers no se agregan otra vez (evita lineas repetidas)
    if not logger.handlers:  # solo entra la primera vez
        manejador = logging.FileHandler(ARCHIVO_LOG, encoding="utf-8")  # escribe en el archivo
        formato = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")  # fecha | nivel | mensaje
        manejador.setFormatter(formato)  # le asignamos el formato al manejador
        logger.addHandler(manejador)  # conectamos el manejador al logger

    return logger  # devolvemos el logger ya configurado

# Un solo logger compartido por todos los modulos
logger = crear_logger()  # se crea al importar este archivo
