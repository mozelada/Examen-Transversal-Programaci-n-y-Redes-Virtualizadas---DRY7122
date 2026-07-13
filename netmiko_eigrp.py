from netmiko import ConnectHandler

# Configuración del dispositivo para Netmiko
# !!! REEMPLAZA CON LA IP REAL DE TU ROUTER CSR1000v !!!
router_datos = {
    'device_type': 'cisco_ios',
    'host': '192.168.56.101',
    'username': 'admin',
    'password': 'cisco',
}

def main():
    print(f"Estableciendo conexión SSH mediante Netmiko con {router_datos['host']}...")
    
    try:
        # 1. Conexión al equipo
        net_connect = net_connect = ConnectHandler(**router_datos)
        print("¡Conexión SSH exitosa!")

        # 2. Configuración de EIGRP Nombrado (IPv4 e IPv6) con AS 100 y pasivas
        print("\nConfigurando EIGRP Nombrado e interfaces pasivas...")
        comandos_eigrp = [
            'router eigrp EXAMEN_DRY7122',
            'address-family ipv4 autonomous-system 100',
            'network 192.168.56.0 0.0.0.255',
            'af-interface GigabitEthernet1',
            'passive-interface',
            'exit-af-interface',
            'exit-address-family',
            'address-family ipv6 autonomous-system 100',
            'af-interface GigabitEthernet1',
            'passive-interface',
            'exit-af-interface',
            'exit-address-family'
        ]
        
        # Enviar comandos de configuración
        salida_config = net_connect.send_config_set(comandos_eigrp)
        print("Configuración de enrutamiento enviada.")

        print("\n=======================================================")
        print(" VERIFICACIÓN DE REQUERIMIENTOS EXAMEN (ÍTEM 7)")
        print("=======================================================")

        # REQUERIMIENTO: Mostrar resultado con 'show running-config section eigrp'
        print("\n1. [Comando: show running-config section eigrp]")
        print("-------------------------------------------------------")
        verificar_eigrp = net_connect.send_command('show running-config section eigrp')
        print(verificar_eigrp)

        # REQUERIMIENTO: Obtener información de IPs y estado de interfaces
        print("\n2. [Comando: show ip interface brief]")
        print("-------------------------------------------------------")
        interfaces_ip = net_connect.send_command('show ip interface brief')
        print(interfaces_ip)

        # REQUERIMIENTO: Obtener el show version
        print("\n3. [Comando: show version]")
        print("-------------------------------------------------------")
        version_sistema = net_connect.send_command('show version')
        # Imprimimos solo las primeras líneas para no saturar la pantalla
        print("\n".join(version_sistema.splitlines()[:10])) 
        print("... [Salida truncada en script para visualización] ...")

        # REQUERIMIENTO: Obtener el running-config completo y guardarlo localmente
        print("\n4. [Comando: show running-config]")
        print("-------------------------------------------------------")
        running_completo = net_connect.send_command('show running-config')
        
        # Lo guardamos en un archivo de texto para demostrar la recolección masiva
        nombre_archivo_backup = "running_config_netmiko.txt"
        with open(nombre_archivo_backup, "w") as f:
            f.write(running_completo)
        print(f"La running-config completa ha sido guardada con éxito en: '{nombre_archivo_backup}'")

        # Cerrar la sesión de forma limpia
        net_connect.disconnect()
        print("\nConexión finalizada correctamente.")

    except Exception as e:
        print(f"Ocurrió un error en la automatización con Netmiko: {e}")

if __name__ == "__main__":
    main()