
from modules.memory import (
    get_memory_summary,
    get_physical_memory,
    get_top_processes,
    get_memory_status
)


print("\n================================")
print("       PC MEDICINE")
print("       MEMORY ANALYZER")
print("================================\n")


# 1. RESUMEN DE MEMORIA

print("1. RESUMEN DE MEMORIA RAM")

memory = get_memory_summary()

for key, value in memory.items():
    print(f"{key}: {value}")


# 2. ESTADO DE MEMORIA

print("\n2. ESTADO DE MEMORIA")

status = get_memory_status()

print(f"Diagnostico: {status}")


# 3. MODULOS FISICOS

print("\n3. MODULOS DE MEMORIA FISICA")

modules = get_physical_memory()

for module in modules:
    print(module)


# 4. PROCESOS CON MAYOR CONSUMO

print("\n4. PROCESOS CON MAYOR CONSUMO DE RAM")

processes = get_top_processes()

for process in processes:

    print(
        f"PID: {process['pid']} | "
        f"Proceso: {process['name']} | "
        f"Memoria: {process['memory_mb']} MB"
    )


print("\n================================")
print("   ANALISIS FINALIZADO")
print("================================")
