import psutil
import time

def bytes_to_gb(value):
    """
    Convierte bytes a gigabytes.
    """
    return round(value / (1024 ** 3), 2)

def format_bytes(value):
    """
    Convierte bytes a una unidad legible.
    """
    units = ["B", "KB", "MB", "GB", "TB"]

    value = float(value)

    for unit in units:
        if value < 1024:
            return f"{value:.2f} {unit}"
        value /= 1024

    return f"{value:.2f} PB"

def get_cpu_info():
    return {
        "usage": psutil.cpu_percent(interval=None),
        "cores": psutil.cpu_count(logical=False),
        "threads": psutil.cpu_count(logical=True),
        "frequency": psutil.cpu_freq().current
        if psutil.cpu_freq() else 0
    }

def get_ram_info():

    memory = psutil.virtual_memory()

    return {
        "total": bytes_to_gb(memory.total),
        "used": bytes_to_gb(memory.used),
        "available": bytes_to_gb(memory.available),
        "percentage": memory.percent
    }

def get_disk_info(path="C:\\"):

    disk = psutil.disk_usage(path)

    return {
        "total": bytes_to_gb(disk.total),
        "used": bytes_to_gb(disk.used),
        "free": bytes_to_gb(disk.free),
        "percentage": disk.percent
    }

def get_network_info():

    network = psutil.net_io_counters()

    return {
        "bytes_sent": network.bytes_sent,
        "bytes_received": network.bytes_recv,
        "sent": format_bytes(network.bytes_sent),
        "received": format_bytes(network.bytes_recv)
    }

def get_disk_activity():

    disk = psutil.disk_io_counters()

    if disk is None:
        return {
            "read": 0,
            "write": 0
        }
    return {
        "read": disk.read_bytes,
        "write": disk.write_bytes
    }

def get_system_uptime():

    boot_time = psutil.boot_time()

    uptime_seconds = int(time.time() - boot_time)

    days = uptime_seconds // 86400
    hours = (uptime_seconds % 86400) // 3600
    minutes = (uptime_seconds % 3600) // 60

    return {
        "days": days,
        "hours": hours,
        "minutes": minutes
    }

def get_monitoring_data():
    """
    Recopila informacion general del rendimiento del equipo.
    """

    return{
        "cpu": get_cpu_info(),
        "ram": get_ram_info(),
        "disk": get_disk_info(),
        "network": get_network_info(),
        "disk_activity": get_disk_activity(),
        "uptime": get_system_uptime()
    }