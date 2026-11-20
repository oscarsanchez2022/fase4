# gestor.py
# Modulo encargado de administrar las listas en memoria de Software FJ.
# Coordina clientes, servicios y reservas aplicando manejo robusto de excepciones
# (try/except/else/finally y encadenamiento) y guardando todo en el archivo de logs.

from cliente import Cliente  # importa la clase Cliente del modulo correspondiente
from reserva import Reserva  # importa la clase Reserva del modulo correspondiente
from registro import logger  # importa el logger unico para escribir en software_fj.log
from excepciones import ErrorSoftwareFJ, ParametroFaltanteError  # excepciones personalizadas


class GestorFJ:  # clase coordinadora que almacena las listas y controla cada operacion
    def __init__(self):  # metodo constructor que inicializa el gestor
        self._clientes = []  # lista interna en memoria para objetos de tipo Cliente
        self._servicios = []  # lista interna en memoria para objetos de tipo Servicio
        self._reservas = []  # lista interna en memoria para objetos de tipo Reserva

    def registrar_cliente(self, nombre, correo, telefono):  # agrega un cliente tras validarlo
        try:  # bloque donde intentamos instanciar el objeto Cliente
            nuevo_cliente = Cliente(nombre, correo, telefono)  # ejecuta las validaciones de Cliente
        except ErrorSoftwareFJ as err:  # captura errores propios si algun dato es invalido
            logger.error(f"No se pudo registrar cliente '{nombre}': {err}")  # guarda el error en el log
            print(f"  [ERROR] {err}")  # muestra el aviso controlado en consola
            return None  # retorna None para que el sistema siga ejecutandose sin caer
        else:  # se ejecuta unicamente si el bloque try termino sin lanzar excepciones
            self._clientes.append(nuevo_cliente)  # guarda el cliente valido en la lista interna
            logger.info(f"Cliente guardado en memoria: {nuevo_cliente.describir()}")  # registra exito
            print(f"  [OK] {nuevo_cliente.describir()}")  # informa en consola
            return nuevo_cliente  # devuelve el objeto Cliente creado
        finally:  # se ejecuta siempre al final, haya ocurrido error o no
            logger.info("Cierre de proceso: registrar_cliente.")  # deja traza de auditoria en el log

    def crear_servicio(self, clase_servicio, *args, **kwargs):  # crea cualquiera de los 3 servicios
        try:  # bloque externo que captura cualquier excepcion propia del sistema
            try:  # bloque interno para detectar si faltaron argumentos al llamar al constructor
                nuevo_servicio = clase_servicio(*args, **kwargs)  # crea Sala, Equipo o Asesoria
            except TypeError as err:  # ocurre cuando faltan parametros obligatorios en Python
                raise ParametroFaltanteError(
                    f"Faltan datos obligatorios para crear el servicio: {err}"
                ) from err  # encadena el TypeError original como causa de nuestra excepcion
        except ErrorSoftwareFJ as err:  # atrapa ServicioInvalidoError o ParametroFaltanteError
            logger.error(f"No se pudo crear servicio: {err}")  # escribe el fallo en software_fj.log
            if err.__cause__ is not None:  # verifica si existe una excepcion encadenada detras
                logger.error(f"  Causa original encadenada: {err.__cause__}")  # guarda la causa
            print(f"  [ERROR] {err}")  # muestra el error en consola sin detener el programa
            return None  # retorna None indicando que no se creo el servicio
        else:  # corre solo cuando el servicio se creo correctamente
            self._servicios.append(nuevo_servicio)  # almacena el servicio en la lista interna
            logger.info(f"Servicio guardado en memoria: {nuevo_servicio.describir()}")  # log de exito
            print(f"  [OK] {nuevo_servicio.describir()}")  # confirma en consola
            return nuevo_servicio  # devuelve el servicio listo para reservar
        finally:  # se ejecuta obligatoriamente al terminar el intento
            logger.info("Cierre de proceso: crear_servicio.")  # registra fin de operacion

    def crear_reserva(self, cliente, servicio, horas):  # asocia un cliente con un servicio por horas
        try:  # intenta construir la reserva validando disponibilidad, cliente y rango de horas
            nueva_reserva = Reserva(cliente, servicio, horas)  # instancia la reserva
        except ErrorSoftwareFJ as err:  # captura errores de reserva, disponibilidad o horas malas
            logger.error(f"No se pudo generar reserva: {err}")  # registra el fallo en el log
            if err.__cause__ is not None:  # si hubo encadenamiento dentro de Reserva
                logger.error(f"  Causa original encadenada: {err.__cause__}")  # tambien lo registra
            print(f"  [ERROR] {err}")  # muestra alerta en pantalla
            return None  # mantiene la aplicacion activa devolviendo None
        else:  # corre unicamente si la reserva paso todas las validaciones
            self._reservas.append(nueva_reserva)  # agrega la reserva a la lista interna
            logger.info(f"Reserva guardada en memoria: {nueva_reserva.describir()}")  # log de exito
            print(f"  [OK] {nueva_reserva.describir()}")  # confirma en consola
            return nueva_reserva  # devuelve la reserva creada
        finally:  # corre siempre al finalizar
            logger.info("Cierre de proceso: crear_reserva.")  # traza de cierre en el log

    def ejecutar_accion(self, reserva, accion, **kwargs):  # ejecuta confirmar, cancelar o procesar
        try:  # intenta invocar dinamicamente el metodo indicado sobre la reserva
            resultado = getattr(reserva, accion)(**kwargs)  # busca el metodo en Reserva y lo ejecuta
        except ErrorSoftwareFJ as err:  # atrapa OperacionNoPermitidaError o CalculoInconsistenteError
            logger.error(f"Fallo al ejecutar '{accion}' en reserva: {err}")  # guarda error en log
            if err.__cause__ is not None:  # revisa si hay causa original encadenada
                logger.error(f"  Causa original encadenada: {err.__cause__}")  # guarda la causa
                print(f"  [ERROR] {err} | Causa: {err.__cause__}")  # muestra error y causa
            else:  # si no hay causa encadenada
                print(f"  [ERROR] {err}")  # muestra solo el mensaje de error
            return None  # continua la ejecucion sin interrupciones
        except AttributeError:  # ocurre si se intenta operar sobre una reserva que fue None
            logger.error(f"Intento de '{accion}' sobre una reserva nula (None).")  # log del fallo
            print("  [ERROR] La reserva no existe o fallo al crearse previamente.")  # aviso en consola
            return None  # continua la ejecucion
        else:  # corre solo si la accion sobre la reserva fue exitosa
            if resultado is not None:  # si la accion devolvio un valor (ej. procesar retorna el costo)
                print(f"  [OK] {accion} completada. Total: ${resultado:,.2f}")  # imprime el valor
            else:  # si la accion no retorna valor (confirmar o cancelar)
                print(f"  [OK] {accion} completada correctamente.")  # confirma la accion
            return resultado  # devuelve el resultado obtenido
        finally:  # se ejecuta siempre
            logger.info(f"Cierre de proceso: ejecutar_accion ({accion}).")  # traza de cierre

    def resumen(self):  # imprime en consola cuantos elementos hay guardados en cada lista interna
        print(
            f"  Total en memoria -> Clientes: {len(self._clientes)} | "
            f"Servicios: {len(self._servicios)} | "
            f"Reservas: {len(self._reservas)}"
        )  # muestra el conteo final de las tres listas
