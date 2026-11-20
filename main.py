# main.py
# Punto de entrada principal del sistema Software FJ (Fase 4 - UNAD).
# Ejecuta secuencialmente 14 operaciones (validas y fallidas) para demostrar
# que el programa maneja excepciones, guarda logs y nunca detiene su ejecucion.

from gestor import GestorFJ  # importa el gestor principal que administra las listas en memoria
from servicios import ServicioSala, ServicioEquipo, ServicioAsesoria  # importa los tres tipos de servicio
from registro import logger, ARCHIVO_LOG  # importa el logger compartido y la ruta del archivo de logs


def iniciar_simulacion():  # funcion principal que ejecuta todas las pruebas paso a paso
    print("============================================================")
    print("   SISTEMA INTEGRAL DE GESTION - SOFTWARE FJ (FASE 4)")
    print("============================================================\n")
    logger.info("=== INICIO DE SIMULACION DEL SISTEMA SOFTWARE FJ ===")  # marca el arranque en el log

    gestor = GestorFJ()  # crea el administrador en memoria (sin uso de base de datos)

    # ------------------------------------------------------------------
    # BLOQUE 1: REGISTRO DE CLIENTES (VALIDOS E INVALIDOS)
    # ------------------------------------------------------------------
    print("--- 1. Registro de Clientes ---")
    # Operacion 1: Registro exitoso de primer cliente
    cliente_1 = gestor.registrar_cliente("Laura Gomez", "laura.gomez@correo.com", "3001234567")

    # Operacion 2: Registro exitoso de segundo cliente
    cliente_2 = gestor.registrar_cliente("Carlos Ruiz", "carlos.ruiz@empresa.co", "3109876543")

    # Operacion 3: Registro FALLIDO de cliente (nombre vacio y correo invalido -> captura ClienteInvalidoError)
    cliente_error = gestor.registrar_cliente("", "correo_sin_arroba", "123")

    # ------------------------------------------------------------------
    # BLOQUE 2: CREACION DE SERVICIOS (CORRECTOS E INCORRECTOS)
    # ------------------------------------------------------------------
    print("\n--- 2. Creacion de Servicios ---")
    # Operacion 4: Creacion exitosa de Sala (capacidad > 10 aplica recargo del 10%)
    sala_ejecutiva = gestor.crear_servicio(ServicioSala, "Sala Ejecutiva Norte", 50000, 15)

    # Operacion 5: Creacion exitosa de Equipo (incluye deposito fijo de $20.000)
    equipo_mac = gestor.crear_servicio(ServicioEquipo, "MacBook Pro M3", 15000, "Computador Portatil")

    # Operacion 6: Creacion exitosa de Asesoria (nivel senior aplica recargo del 25%)
    asesoria_cloud = gestor.crear_servicio(
        ServicioAsesoria, "Arquitectura Cloud", 80000, "Nube AWS", "senior"
    )

    # Operacion 7: Creacion FALLIDA de servicio por tarifa negativa (captura ServicioInvalidoError)
    servicio_tarifa_mala = gestor.crear_servicio(ServicioSala, "Sala Fantasma", -10000, 8)

    # Operacion 8: Creacion FALLIDA por parametro faltante (prueba encadenamiento TypeError -> ParametroFaltanteError)
    servicio_incompleto = gestor.crear_servicio(ServicioSala, "Sala Sin Capacidad", 40000)

    # ------------------------------------------------------------------
    # BLOQUE 3: CREACION Y PROCESAMIENTO DE RESERVAS (EXITOSAS Y FALLIDAS)
    # ------------------------------------------------------------------
    print("\n--- 3. Creacion y Gestion de Reservas ---")
    # Operacion 9: Reserva EXITOSA de Sala para cliente_1 por 4 horas
    reserva_1 = gestor.crear_reserva(cliente_1, sala_ejecutiva, 4)

    # Operacion 10: Confirmar y procesar reserva_1 con impuesto (19%) y descuento (10%)
    gestor.ejecutar_accion(reserva_1, "confirmar")  # cambia el estado a confirmada
    gestor.ejecutar_accion(reserva_1, "procesar", impuesto=0.19, descuento=0.10)  # aplica sobrecarga con impuesto y descuento

    # Operacion 11: Reserva FALLIDA por horas fuera de rango (Asesoria solo permite 1 a 4 horas, pedimos 10)
    reserva_horas_mal = gestor.crear_reserva(cliente_2, asesoria_cloud, 10)

    # Operacion 12: Reserva FALLIDA por servicio no disponible
    equipo_mac.marcar_disponible(False)  # desactivamos el equipo manualmente
    reserva_no_disponible = gestor.crear_reserva(cliente_2, equipo_mac, 5)  # lanza ServicioNoDisponibleError

    # Operacion 13: Operacion NO PERMITIDA (intentar cancelar una reserva que ya fue procesada)
    gestor.ejecutar_accion(reserva_1, "cancelar")  # lanza OperacionNoPermitidaError

    # Operacion 14: Accion sobre reserva nula (reserva_horas_mal fue None -> captura AttributeError)
    gestor.ejecutar_accion(reserva_horas_mal, "confirmar")

    # Operacion 15: Segunda reserva EXITOSA (Asesoria para cliente_2 por 2 horas solo con impuesto)
    reserva_2 = gestor.crear_reserva(cliente_2, asesoria_cloud, 2)
    gestor.ejecutar_accion(reserva_2, "confirmar")  # confirma la segunda reserva
    gestor.ejecutar_accion(reserva_2, "procesar", impuesto=0.19)  # usa sobrecarga sin descuento

    # ------------------------------------------------------------------
    # RESUMEN FINAL EN MEMORIA
    # ------------------------------------------------------------------
    print("\n--- Resumen Final de Registros en Memoria ---")
    gestor.resumen()  # muestra cuantos clientes, servicios y reservas validas quedaron guardados
    print(f"\nEjecucion finalizada sin interrupciones. Logs guardados en: {ARCHIVO_LOG}")
    logger.info("=== FIN DE SIMULACION DEL SISTEMA SOFTWARE FJ ===")  # cierra el registro en el log


if __name__ == "__main__":  # verifica que este archivo se ejecute directamente como programa principal
    iniciar_simulacion()  # arranca toda la simulacion
