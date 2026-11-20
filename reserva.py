# reserva.py
# Clase Reserva: une cliente, servicio, duracion y estado.
# Aqui se aplican validaciones, try/except/else/finally y encadenamiento de excepciones.

from entidad import Entidad  # Reserva hereda de Entidad para obtener id y obligar describir()
from cliente import Cliente  # Verifica que el cliente recibido sea una instancia valida
from servicios import Servicio  # Verifica que el servicio recibido sea una instancia valida
from registro import logger  # Logger compartido del sistema para registrar eventos
from excepciones import (  # Excepciones personalizadas usadas en este modulo
    ReservaInvalidaError,
    ServicioNoDisponibleError,
    OperacionNoPermitidaError,
    CalculoInconsistenteError,
    ServicioInvalidoError,
)

# Estados validos del ciclo de vida de una reserva
PENDIENTE = "PENDIENTE"  # Estado inicial al crear la reserva
CONFIRMADA = "CONFIRMADA"  # Lista para calcular costo y procesar
CANCELADA = "CANCELADA"  # Cancelada; no permite nuevas operaciones
PROCESADA = "PROCESADA"  # Costo calculado y cerrado; no permite cambios


class Reserva(Entidad):  # Clase Reserva que hereda de Entidad
    def __init__(self, cliente, servicio, horas):  # Inicializa la reserva con cliente, servicio y horas
        # Valida que cliente y servicio correspondan a las clases esperadas
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("La reserva necesita un cliente valido.")
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("La reserva necesita un servicio valido.")

        # Impide reservar servicios marcados como no disponibles
        if not servicio.disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{servicio.nombre}' no esta disponible."
            )

        # Valida que horas sea un numero positivo y no un booleano (en Python bool hereda de int)
        if isinstance(horas, bool) or not isinstance(horas, (int, float)) or horas <= 0:
            raise ReservaInvalidaError("La duracion en horas debe ser un numero mayor que cero.")

        # Encadenamiento de excepciones: si falla la regla de horas del servicio,
        # se lanza ReservaInvalidaError conservando la causa original (raise ... from ...)
        try:
            servicio.validar_parametros(horas)
        except ServicioInvalidoError as error:
            raise ReservaInvalidaError(
                f"No se pudo crear la reserva: {error}"
            ) from error

        self._cliente = cliente  # Almacena el objeto Cliente
        self._servicio = servicio  # Almacena el objeto Servicio
        self._horas = horas  # Almacena la cantidad de horas solicitadas
        self._estado = PENDIENTE  # Toda reserva nueva inicia en PENDIENTE
        self._costo = None  # El costo final se asigna al procesar la reserva
        super().__init__()  # Asigna el id unico una vez validados los datos

    @property  # Acceso de solo lectura al cliente
    def cliente(self):
        return self._cliente

    @property  # Acceso de solo lectura al servicio
    def servicio(self):
        return self._servicio

    @property  # Acceso de solo lectura al estado actual
    def estado(self):
        return self._estado

    @property  # Acceso de solo lectura al costo calculado
    def costo(self):
        return self._costo

    def confirmar(self):  # Cambia el estado de PENDIENTE a CONFIRMADA
        # Solo se puede confirmar una reserva que aun este pendiente
        if self._estado != PENDIENTE:
            raise OperacionNoPermitidaError(
                f"No se puede confirmar una reserva en estado {self._estado}."
            )
        self._estado = CONFIRMADA  # Actualiza el estado a CONFIRMADA
        logger.info(f"Reserva #{self.id} confirmada.")  # Registra la confirmacion en el log

    def cancelar(self):  # Cancela la reserva si su estado actual lo permite
        # No se puede cancelar una reserva ya procesada ni una ya cancelada
        if self._estado in (PROCESADA, CANCELADA):
            raise OperacionNoPermitidaError(
                f"No se puede cancelar una reserva en estado {self._estado}."
            )
        self._estado = CANCELADA  # Actualiza el estado a CANCELADA
        logger.info(f"Reserva #{self.id} cancelada.")  # Registra la cancelacion en el log

    def procesar(self, impuesto=0.0, descuento=0.0):  # Calcula el costo final y cierra la reserva
        """Calcula el costo final de la reserva y la marca como PROCESADA."""
        # Solo se procesan reservas previamente confirmadas
        if self._estado != CONFIRMADA:
            raise OperacionNoPermitidaError(
                "Solo se pueden procesar reservas confirmadas."
            )

        try:
            # Calcula el costo aplicando horas, descuento e impuesto opcionales
            costo_calculado = self._servicio.costo_final(self._horas, impuesto, descuento)
        except CalculoInconsistenteError as error:
            # Encadena el error de calculo dentro de una excepcion de operacion del sistema
            raise OperacionNoPermitidaError(
                f"No se pudo procesar la reserva #{self.id}."
            ) from error
        else:
            # Se ejecuta solo si costo_final() termino sin lanzar excepciones
            self._costo = costo_calculado
            self._estado = PROCESADA
            logger.info(
                f"Reserva #{self.id} procesada. Costo final: ${costo_calculado:,.2f}"
            )
            return self._costo
        finally:
            # Se ejecuta siempre al salir del bloque try/except/else
            logger.info(f"Se intento procesar la reserva #{self.id}.")

    def describir(self):  # Implementa el metodo abstracto exigido por Entidad
        return (
            f"Reserva #{self.id} | {self._cliente.nombre} | "
            f"{self._servicio.nombre} | {self._horas} h | {self._estado}"
        )
