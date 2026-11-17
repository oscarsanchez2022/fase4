# excepciones.py
# Aqui estan todas las excepciones personalizadas del sistema .
# Todas heredan de ErrorSoftwareFJ para poder capturarlas juntas si hace falta.

class ErrorSoftwareFJ(Exception):
    """Excepcion base de todo el sistema."""

class ClienteInvalidoError(ErrorSoftwareFJ):
    """Se usa cuando los datos de un cliente no pasan las validaciones."""

class ServicioInvalidoError(ErrorSoftwareFJ):
    """Se usa cuando un servicio se crea con datos incorrectos."""

class ServicioNoDisponibleError(ErrorSoftwareFJ):
    """Se usa cuando se intenta reservar un servicio que no esta disponible."""

class ReservaInvalidaError(ErrorSoftwareFJ):
    """Se usa cuando una reserva se crea con datos incorrectos."""

class OperacionNoPermitidaError(ErrorSoftwareFJ):
    """Se usa cuando se intenta una accion que el estado de la reserva no permite."""

class CalculoInconsistenteError(ErrorSoftwareFJ):
    """Se usa cuando un calculo de costos da un resultado que no tiene sentido."""
