from ncclient import manager
import xmltodict
import xml.dom.minidom

# Configuración de conexión al router CSR1000v
ROUTER_IP = "192.168.56.101" 
ROUTER_PORT = 830  # Puerto estándar de NETCONF
USER = "admin"
PASS = "cisco"

nuevo_hostname = "Zelada_Montserrat"

config_hostname_xml = f"""
<config>
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <hostname>{nuevo_hostname}</hostname>
    </native>
</config>
"""

# 2. Configuración XML para crear la interfaz Loopback 11 (11.11.11.11/32)
config_loopback_xml = """
<config>
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
            <loopback>
                <name>11</name>
                <description>Creada via NETCONF - Item 4</description>
                <ip>
                    <address>
                        <primary>
                            <address>11.11.11.11</address>
                            <mask>255.255.255.255</mask>
                        </primary>
                    </address>
                </ip>
            </loopback>
        </interface>
    </native>
</config>
"""

def main():
    print(f"Estableciendo conexión SSH/NETCONF con el router {ROUTER_IP}...")
    
    try:
        # Establecemos la conexión NETCONF mediante SSH
        with manager.connect(
            host=ROUTER_IP,
            port=ROUTER_PORT,
            username=USER,
            password=PASS,
            hostkey_verify=False,
            device_params={'name': 'iosxe'}
        ) as m:
            
            print("¡Conexión NETCONF establecida con éxito!")
            
            # Aplicar cambio de Hostname
            print(f"Cambiando el hostname a: {nuevo_hostname}...")
            respuesta_hostname = m.edit_config(target='running', config=config_hostname_xml)
            print("Resultado Hostname:", respuesta_hostname)
            
            # Aplicar creación de Loopback 11
            print("Configurando interfaz Loopback 11 (11.11.11.11/32)...")
            respuesta_loopback = m.edit_config(target='running', config=config_loopback_xml)
            print("Resultado Loopback 11:", respuesta_loopback)
            
            print("\n==============================================")
            print("¡Configuraciones aplicadas de forma exitosa!")
            print("==============================================")

    except Exception as e:
        print(f"Error al conectarse o interactuar con el router: {e}")

if __name__ == "__main__":
    main()