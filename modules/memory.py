import psutil
import wmi

def get_memory_summary():
    """
    Obtiene el estado general de la memoria RAM.
    """

    memory = psutil.virtual_memory()

    return {
        "total": round(memory.total / (1024 ** 3), 2),
        "used" : round(memory.used / (1024 ** 3), 2),
        "available": round(memory.available / (1024 ** 3), 2),
        "percent" : memory.percent
    }

