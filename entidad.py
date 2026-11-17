# entidad.py
# Clase abstracta que representa cualquier entidad general del sistema (clientes, servicios y reservas comparten un id y una descripcion).

from abc import ABC, abstractmethod  # ABC y abstractmethod sirven para crear clases abstractas

class Entidad(ABC):  # clase abstracta: no se puede crear un objeto directamente de ella
    # Contador compartido por todas las entidades para que cada id sea diferente
    _contador = 0  # empieza en cero y sube con cada entidad nueva

    def __init__(self):  # constructor de la entidad
        Entidad._contador += 1  # sumamos uno al contador compartido
        self._id = Entidad._contador  # guardamos el numero como id (atributo privado)

    @property  # permite leer el id como si fuera un atributo normal: objeto.id
    def id(self):
        # Solo lectura: no hay setter, asi que el id no se puede cambiar desde afuera
        return self._id  # devuelve el id guardado

    @abstractmethod  # obliga a que cada clase hija escriba su propia version
    def describir(self):
        """Cada clase hija debe devolver un texto que la describa."""
