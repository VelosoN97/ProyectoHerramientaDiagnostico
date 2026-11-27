
from modules.monitoring import get_monitoring_data

data = get_monitoring_data()

print("\n")
print("=" * 50)
print("PC MEDICINE - MONITOREO DEL SISTEMA")
print("=" * 50)

print("\nPROCESADOR")

for key, value in data["cpu"].items():
    print(f"{key}: {value}")

print("\nMEMORIA RAM")

for key, value in data["ram"].items():
    print(f"{key}: {value}")

print("\nALMACENAMIENTO")

for key, value in data["disk"].items():
    print(f"{key}: {value}")

print("\nRED")

for key, value in data["network"].items():
    print(f"{key}: {value}")

print("\nACTIVIDAD DEL DISCO")

for key, value in data["disk_activity"].items():
    print(f"{key}: {value}")

print("\nTIEMPO DE ACTIVIDAD DEL EQUIPO")

for key, value in data["uptime"].items():
    print(f"{key}: {value}")

print("\n")
print("=" * 50)
print("MONITOREO COMPLETADO")
print("=" * 50)