vlan = int(input("Ingrese el número de VLAN a consultar: "))

if 1 <= vlan <= 1005:
    print(f"La VLAN {vlan} pertenece al Rango Normal.")
elif 1006 <= vlan <= 4094:
    print(f"La VLAN {vlan} pertenece al Rango Extendido.")
else:
    print("Número de VLAN no válido para los estándares tradicionales (0, 4095, o fuera de rango).")