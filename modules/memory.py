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


def get_physical_memory():
    """
    Obtiene información de los módulos de memoria
    física mediante WMI.
    """

    try:
        connection = wmi.WMI()

        modules = connection.Win32_PhysicalMemory()

        memories = []

        for module in modules:
            memories.append({
                "manufacturer": module.Manufacturer or "No disponible",
                "part_number": module.PartNumber or "No disponible",
                "capacity": round(
                    int(module.Capacity) / (1024 ** 3), 2
                ),
                "speed": module.Speed,
                "device": module.DeviceLocator
            })

        return memories

    except Exception as error:
        print(f"Error obteniendo memoria física: {error}")
        return []

def get_top_processes(limit=10):
    """
    Obtiene los procesos que más memoria RAM consumen.
    """

    processes = []

    for process in psutil.process_iter(
        ["pid", "name", "memory_info"]
    ):
        try:
            information = process.info
            memory_info = information["memory_info"]

            if memory_info is None:
                continue

            memory_mb = round(
                memory_info.rss / (1024 ** 2), 2
            )

            processes.append({
                "pid": information["pid"],
                "name": information["name"] or "Desconocido",
                "memory_mb": memory_mb
            })

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess
            ):
                continue
    processes.sort(
        key=lambda process: process["memory_db"],
        reverse=True
    )

    return processes[:limit]
