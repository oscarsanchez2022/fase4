# servicios.py
# Clase abstracta Servicio y tres servicios especializados que heredan de ella.
# Aqui vemos el polimorfismo, cada servicio calcula su costo y valida a su manera.

from abc import abstractmethod  # para marcar metodos que las hijas deben escribir

from entidad import Entidad  # Servicio hereda de Entidad
from excepciones import ServicioInvalidoError, CalculoInconsistenteError  # excepciones de este modulo

class Servicio(Entidad):  # clase abstracta de la que salen los tres servicios
    def __init__(self, nombre, tarifa_hora):  # datos comunes a todos los servicios
        # Validaciones comunes a todos los servicios
        if not isinstance(nombre, str) or not nombre.strip():  # el nombre debe ser texto no vacio
            raise ServicioInvalidoError("El servicio necesita un nombre.")  # nombre incorrecto
        # La tarifa debe ser numero mayor que cero (bool se excluye porque True seria 1)
        if not isinstance(tarifa_hora, (int, float)) or isinstance(tarifa_hora, bool) or tarifa_hora <= 0:
            raise ServicioInvalidoError("La tarifa por hora debe ser un numero mayor que cero.")  # tarifa mala
        self._nombre = nombre.strip()  # guarda el nombre limpio
        self._tarifa_hora = float(tarifa_hora)  # guarda la tarifa como decimal
        self._disponible = True  # todo servicio nuevo empieza disponible
        super().__init__()  # el id se asigna al final, cuando los datos ya son validos

    @property  # lectura del nombre
    def nombre(self):
        return self._nombre  # atributo privado

    @property  # lectura de la tarifa
    def tarifa_hora(self):
        return self._tarifa_hora  # atributo privado

    @property  # lectura de la disponibilidad
    def disponible(self):
        return self._disponible  # atributo privado

    def marcar_disponible(self, valor):  # activa o desactiva el servicio
        self._disponible = bool(valor)  # se convierte a True o False

    @abstractmethod  # cada servicio define sus propios limites de horas
    def validar_parametros(self, horas):
        """Debe lanzar excepcion si las horas no cumplen con el servicio."""

    @abstractmethod  # cada servicio calcula su costo base a su manera
    def calcular_costo(self, horas):
        """Costo base del servicio, sin impuestos ni descuentos."""

    # Sobrecarga: Python no tiene sobrecarga se simula con
    # parametros opcionales. Se puede llamar de tres formas:
    #   costo_final(horas)
    #   costo_final(horas, impuesto)
    #   costo_final(horas, impuesto, descuento)
    def costo_final(self, horas, impuesto=0.0, descuento=0.0):  # impuesto y descuento son opcionales
        # Impuesto y descuento se manejan como porcentaje entre 0 y 1
        if not (0 <= impuesto <= 1):  # el impuesto debe estar entre 0% y 100%
            raise CalculoInconsistenteError(f"El impuesto {impuesto} debe estar entre 0 y 1.")  # impuesto raro
        if not (0 <= descuento <= 1):  # el descuento debe estar entre 0% y 100%
            raise CalculoInconsistenteError(f"El descuento {descuento} debe estar entre 0 y 1.")  # descuento raro

        self.validar_parametros(horas)  # polimorfismo: cada servicio valida distinto
        base = self.calcular_costo(horas)  # polimorfismo: cada servicio calcula distinto
        total = base * (1 - descuento) * (1 + impuesto)  # aplica descuento y luego impuesto

        # Un costo en cero o negativo no tiene sentido en este sistema
        if total <= 0:  # revisa que el resultado sea valido
            raise CalculoInconsistenteError("El costo calculado no es valido (menor o igual a cero).")  # total malo
        return round(total, 2)  # devuelve el total con dos decimales

class ServicioSala(Servicio):  # servicio de reserva de salas
    """Reserva de salas. Las salas grandes tienen un recargo."""

    def __init__(self, nombre, tarifa_hora, capacidad):  # agrega la capacidad a los datos comunes
        super().__init__(nombre, tarifa_hora)  # el constructor de Servicio valida nombre y tarifa
        if not isinstance(capacidad, int) or capacidad <= 0:  # capacidad debe ser entero positivo
            raise ServicioInvalidoError("La capacidad de la sala debe ser un entero positivo.")  # capacidad mala
        self._capacidad = capacidad  # guarda la capacidad

    def validar_parametros(self, horas):  # limites propios de las salas
        # Una sala se puede reservar de 1 a 8 horas
        if not isinstance(horas, (int, float)) or not (1 <= horas <= 8):  # revisa tipo y rango
            raise ServicioInvalidoError("Las salas se reservan entre 1 y 8 horas.")  # horas fuera de rango

    def calcular_costo(self, horas):  # costo base de una sala
        base = self._tarifa_hora * horas  # tarifa por horas
        if self._capacidad > 10:  # sala grande
            base *= 1.10  # recargo del 10% para salas de mas de 10 personas
        return base  # devuelve el costo base

    def describir(self):  # texto que describe la sala
        return f"Sala '{self.nombre}' para {self._capacidad} personas, ${self.tarifa_hora:,.0f} por hora"

class ServicioEquipo(Servicio):  # servicio de alquiler de equipos
    """Alquiler de equipos. Incluye un deposito fijo por el equipo."""

    DEPOSITO = 20000  # valor fijo que se suma al alquiler

    def __init__(self, nombre, tarifa_hora, tipo_equipo):  # agrega el tipo de equipo
        super().__init__(nombre, tarifa_hora)  # valida nombre y tarifa
        if not isinstance(tipo_equipo, str) or not tipo_equipo.strip():  # tipo debe ser texto no vacio
            raise ServicioInvalidoError("Hay que indicar el tipo de equipo.")  # tipo incorrecto
        self._tipo_equipo = tipo_equipo.strip()  # guarda el tipo de equipo

    def validar_parametros(self, horas):  # limites propios de los equipos
        # Un equipo se alquila de 1 a 72 horas (3 dias)
        if not isinstance(horas, (int, float)) or not (1 <= horas <= 72):  # revisa tipo y rango
            raise ServicioInvalidoError("Los equipos se alquilan entre 1 y 72 horas.")  # horas fuera de rango

    def calcular_costo(self, horas):  # costo base de un equipo
        return self._tarifa_hora * horas + self.DEPOSITO  # tarifa por horas mas el deposito

    def describir(self):  # texto que describe el servicio
        return f"Alquiler de {self._tipo_equipo} ({self.nombre}), ${self.tarifa_hora:,.0f} por hora mas deposito"

class ServicioAsesoria(Servicio):  # servicio de asesorias especializadas
    """Asesorias especializadas. Si el asesor es senior cuesta mas."""

    def __init__(self, nombre, tarifa_hora, especialidad, nivel="junior"):  # nivel es opcional
        super().__init__(nombre, tarifa_hora)  # valida nombre y tarifa
        if not isinstance(especialidad, str) or not especialidad.strip():  # especialidad no vacia
            raise ServicioInvalidoError("La asesoria necesita una especialidad.")  # especialidad mala
        if nivel not in ("junior", "senior"):  # solo dos niveles permitidos
            raise ServicioInvalidoError("El nivel del asesor debe ser 'junior' o 'senior'.")  # nivel malo
        self._especialidad = especialidad.strip()  # guarda la especialidad
        self._nivel = nivel  # guarda el nivel

    def validar_parametros(self, horas):  # limites propios de las asesorias
        # Una asesoria dura entre 1 y 4 horas
        if not isinstance(horas, (int, float)) or not (1 <= horas <= 4):  # revisa tipo y rango
            raise ServicioInvalidoError("Las asesorias duran entre 1 y 4 horas.")  # horas fuera de rango

    def calcular_costo(self, horas):  # costo base de una asesoria
        base = self._tarifa_hora * horas  # tarifa por horas
        if self._nivel == "senior":  # asesor senior
            base *= 1.25  # los asesores senior cobran 25% mas
        return base  # devuelve el costo base

    def describir(self):  # texto que describe la asesoria
        return f"Asesoria de {self._especialidad} (nivel {self._nivel}), ${self.tarifa_hora:,.0f} por hora"
