from modules.hardware import get_hardware_info

hardware = get_hardware_info()

for category, information in hardware.items():

    print("\n")
    print("=" * 50)
    print(category.upper())
    print("=" * 50)

    if isinstance(information, list):

        for component in information:

            for key, value in component.items():
                print(f"{key}: {value}")

            print("-" * 30)

    elif isinstance(information, dict):

        for key, value in information.items():
            print(f"{key}: {value}")