# cliente.py
# Clase Cliente con validaciones y datos personales encapsulados.

import re  # modulo de expresiones regulares, sirve para revisar formatos de texto

from entidad import Entidad  # clase abstracta de la que hereda Cliente
from excepciones import ClienteInvalidoError, ParametroFaltanteError  # excepciones que usamos aqui


class Cliente(Entidad):  # Cliente hereda de Entidad
    def __init__(self, nombre, correo, telefono):  # constructor con los datos personales
        # Al asignar con self.nombre se ejecuta el setter, que valida antes de guardar
        self.nombre = nombre  # valida y guarda el nombre
        self.correo = correo  # valida y guarda el correo
        self.telefono = telefono  # valida y guarda el telefono
        # El id se asigna al final para no gastar numeros en clientes invalidos
        super().__init__()  # llama al constructor de Entidad

    # ---------- nombre ----------
    @property  # getter: permite leer cliente.nombre
    def nombre(self):
        return self._nombre  # atributo privado

    @nombre.setter  # setter: se ejecuta cuando se escribe cliente.nombre = algo
    def nombre(self, valor):
        if valor is None or valor == "":  # si no llego ningun dato
            raise ParametroFaltanteError("Falta el nombre del cliente.")  # error de dato faltante
        # Debe ser texto y de al menos 3 caracteres
        if not isinstance(valor, str) or len(valor.strip()) < 3:  # revisa tipo y largo
            raise ClienteInvalidoError("El nombre debe tener al menos 3 letras.")  # nombre muy corto
        # Solo letras y espacios (se permiten tildes y la ñ)
        if not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñ ]+", valor.strip()):  # patron de letras
            raise ClienteInvalidoError("El nombre solo puede tener letras y espacios.")  # tiene simbolos o numeros
        self._nombre = valor.strip()  # guarda el nombre sin espacios sobrantes

    # ---------- correo ----------
    @property  # getter del correo
    def correo(self):
        return self._correo  # atributo privado

    @correo.setter  # setter del correo
    def correo(self, valor):
        if valor is None or valor == "":  # si no llego el correo
            raise ParametroFaltanteError("Falta el correo del cliente.")  # error de dato faltante
        # Revision simple del formato texto@dominio.algo
        if not isinstance(valor, str) or not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", valor.strip()):  # formato
            raise ClienteInvalidoError(f"El correo '{valor}' no tiene un formato valido.")  # correo mal escrito
        self._correo = valor.strip().lower()  # se guarda en minusculas

    # ---------- telefono ----------
    @property  # getter del telefono
    def telefono(self):
        return self._telefono  # atributo privado

    @telefono.setter  # setter del telefono
    def telefono(self, valor):
        if valor is None or valor == "":  # si no llego el telefono
            raise ParametroFaltanteError("Falta el telefono del cliente.")  # error de dato faltante
        # Solo digitos, entre 7 y 10
        if not isinstance(valor, str) or not re.fullmatch(r"\d{7,10}", valor.strip()):  # patron de digitos
            raise ClienteInvalidoError("El telefono debe tener entre 7 y 10 digitos.")  # telefono incorrecto
        self._telefono = valor.strip()  # guarda el telefono limpio

    def describir(self):  # implementa el metodo abstracto de Entidad
        return f"Cliente #{self.id}: {self.nombre} ({self.correo})"  # texto con id, nombre y correo
