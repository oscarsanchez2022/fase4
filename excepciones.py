# Excepciones.py  Aqui estan todas las excepciones personalizadas del sistema
# Todas heredan de ErrorSoftwareFJ para poder capturarlas juntas si hace falta.

class ErrorSoftwareFJ(Exception):  # excepcion base: de aqui salen todas las demas
    """Excepcion base de todo el sistema."""  # texto que explica para que sirve

class ClienteInvalidoError(ErrorSoftwareFJ):  # hereda de la base del sistema
    """Se usa cuando los datos de un cliente no pasan las validaciones."""

class ServicioInvalidoError(ErrorSoftwareFJ):  # errores al crear o validar servicios
    """Se usa cuando un servicio se crea con datos incorrectos."""

class ServicioNoDisponibleError(ErrorSoftwareFJ):  # el servicio existe pero esta apagado
    """Se usa cuando se intenta reservar un servicio que no esta disponible."""

class ReservaInvalidaError(ErrorSoftwareFJ):  # errores al crear una reserva
    """Se usa cuando una reserva se crea con datos incorrectos."""

class OperacionNoPermitidaError(ErrorSoftwareFJ):  # accion que el estado no permite
    """Se usa cuando se intenta una accion que el estado de la reserva no permite."""

class CalculoInconsistenteError(ErrorSoftwareFJ):  # costos que no tienen sentido
    """Se usa cuando un calculo de costos da un resultado que no tiene sentido."""

class ParametroFaltanteError(ErrorSoftwareFJ):  # falta un dato obligatorio
    """Se usa cuando falta un dato obligatorio al crear un objeto."""
