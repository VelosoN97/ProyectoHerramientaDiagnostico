import platform
import wmi

def get_wmi_connection():
    """
    Establece la conexion con Windows Management Instrumentation.
    """

    return wmi.WMI()

def safe_value(value, default="No disponible"):
    """
    Evita mostrar valores vacios o inexistentes.
    """

    if value is None or value == "":
        return default

    return value

def bytes_to_gb(value):
    """
    Convierte bytes a gigabytes.
    """
    try:
        return round(int(value) / (1024 ** 3), 2)
    except (TypeError, ValueError):
        return 0

def get_cpu_info():

    computer = get_wmi_connection()
    processors = computer.Win32_Processor()

    cpu_list = []

    for cpu in processors:

        cpu_list.append({
            "name": safe_value(cpu.Name),
            "manufacturer": safe_value(cpu.Manufacturer),
            "cores": safe_value(cpu.NumberOfCores),
            "threads": safe_value(cpu.NumberOfLogicalProcessors),
            "max_frequency": safe_value(cpu.MaxClockSpeed),
            "architecture": safe_value(cpu.Architecture)
        })
    return cpu_list

def get_motherboard_info():

    computer = get_wmi_connection()

    boards = computer.Win32_BaseBoard()

    motherboard_list = []

    for board in boards:

        motherboard_list.append({
            "manufacturer": safe_value(board.Manufacturer),
            "product": safe_value(board.Product),
            "serial_number": safe_value(board.SerialNumber),
            "version": safe_value(board.Version)
        })
    return motherboard_list

def get_bios_info():

    computer = get_wmi_connection()

    bios_list = computer.Win32_BIOS()

    result = []

    for bios in bios_list:

        result.append({
            "manufacturer": safe_value(bios.Manufacturer),
            "version": safe_value(bios.SMBIOSBIOSVersion),
            "release_date": safe_value(bios.ReleaseDate),
            "serial_number": safe_value(bios.SerialNumber)
        })
    return result

def get_gpu_info():

    computer = get_wmi_connection()

    video_controllers = computer.Win32_VideoController()

    gpu_list =  []

    for gpu in video_controllers:

        gpu_list.append({
            "name": safe_value(gpu.Name),
            "manufacturer": safe_value(gpu.AdapterCompatibility),
            "memory_gb": bytes_to_gb(gpu.AdapterRAM),
            "driver_version": safe_value(gpu.DriverVersion),
            "video_processor": safe_value(gpu.VideoProcessor)
        })
    return gpu_list

def get_ram_info():

    computer = get_wmi_connection()

    memory_modules = computer.Win32_PhysicalMemory()

    ram_list = []

    for memory in memory_modules:

        ram_list.append({
            "manufacturer": safe_value(memory.Manufacturer),
            "part_number": safe_value(memory.PartNumber),
            "capacity_gb": bytes_to_gb(memory.Capacity),
            "speed": safe_value(memory.Speed),
            "device": safe_value(memory.DeviceLocator)
        })
    return ram_list

def get_disk_info():

    computer = get_wmi_connection()

    drives = computer.Win32_DiskDrive()

    disk_list = []

    for drive in drives:

        disk_list.append({
            "model": safe_value(drive.Model),
            "manufacturer": safe_value(drive.Manufacturer),
            "interface": safe_value(drive.InterfaceType),
            "media_type": safe_value(drive.MediaType),
            "capacity_gb": bytes_to_gb(drive.Size),
            "serial_number": safe_value(drive.SerialNumber)
        })
    return disk_list

def get_hardware_info():
    """
    Obtiene un resumen general del hardware del equipo.
    """

    return{
        "system": {
            "computer_game": platform.node(),
            "system": platform.system(),
            "version": platform.version(),
            "architecture": platform.machine()
        },

        "cpu": get_cpu_info(),
        "motherboard": get_motherboard_info(),
        "bios": get_bios_info(),
        "gpu": get_gpu_info(),
        "ram": get_ram_info(),
        "disks": get_disk_info()
    }