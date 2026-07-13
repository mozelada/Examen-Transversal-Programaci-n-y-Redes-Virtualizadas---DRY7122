import requests
import urllib.parse

# Configuración inicial de la API
API_KEY = "f81c0ad6-bca3-41b3-bc2a-2ee426fff90b"
URL_GEOCODE = "https://graphhopper.com/api/1/geocode?"
URL_ROUTING = "https://graphhopper.com/api/1/route?"

def obtener_coordenadas(ciudad):
    """Obtiene las coordenadas (lat, lng) de una ciudad dada."""
    query = {
        "q": ciudad,
        "locale": "es",
        "limit": 1,
        "key": API_KEY
    }
    url = URL_GEOCODE + urllib.parse.urlencode(query)
    respuesta = requests.get(url).json()
    
    if "hits" in respuesta and len(respuesta["hits"]) > 0:
        lat = respuesta["hits"][0]["point"]["lat"]
        lng = respuesta["hits"][0]["point"]["lng"]
        nombre_formateado = respuesta["hits"][0]["name"]
        pais = respuesta["hits"][0].get("country", "")
        return lat, lng, f"{nombre_formateado}, {pais}"
    return None

def main():
    print("==================================================")
    print("   Calculador de Rutas Chile - Argentina (DRY7122)")
    print("==================================================")
    
    while True:
        print("\n--- Nueva Consulta (Presione 's' para salir) ---")
        ciudad_origen = input("Ciudad de Origen: ").strip()
        if ciudad_origen.lower() == 's':
            print("Saliendo del programa. ¡Buen viaje!")
            break
            
        ciudad_destino = input("Ciudad de Destino: ").strip()
        if ciudad_destino.lower() == 's':
            print("Saliendo del programa. ¡Buen viaje!")
            break

        # Seleccionar medio de transporte
        print("\nSeleccione el medio de transporte:")
        print("1. Auto (car)")
        print("2. Bicicleta (bike)")
        print("3. Caminando (foot)")
        opcion = input("Opción (1-3): ").strip()
        
        if opcion == "1":
            perfil = "car"
        elif opcion == "2":
            perfil = "bike"
        elif opcion == "3":
            perfil = "foot"
        else:
            print("Opción no válida. Se utilizará 'car' por defecto.")
            perfil = "car"

        print("\nBuscando localizaciones...")
        origen_datos = obtener_coordenadas(ciudad_origen)
        destino_datos = obtener_coordenadas(ciudad_destino)

        if not origen_datos or not destino_datos:
            print("Error: No se pudo encontrar alguna de las ciudades. Intente nuevamente.")
            continue

        lat_orig, lng_orig, nombre_orig = origen_datos
        lat_dest, lng_dest, nombre_dest = destino_datos

        print(f"Desde: {nombre_orig}")
        print(f"Hasta: {nombre_dest}")

        # Consultar la ruta (Routing API)
        # Formato de puntos requerido por GraphHopper: point=lat,lng
        url_ruta = f"{URL_ROUTING}point={lat_orig},{lng_orig}&point={lat_dest},{lng_dest}&vehicle={perfil}&locale=es&instructions=true&key={API_KEY}"
        
        respuesta_ruta = requests.get(url_ruta).json()

        if "paths" in respuesta_ruta:
            ruta = respuesta_ruta["paths"][0]
            
            # Distancia en metros transformada a km y millas
            distancia_km = ruta["distance"] / 1000
            distancia_millas = distancia_km * 0.621371
            
            # Duración en milisegundos transformada a horas/minutos
            tiempo_ms = ruta["time"]
            horas = int(tiempo_ms / 3600000)
            minutos = int((tiempo_ms % 3600000) / 60000)
            
            print("\n================ DETALLES DEL VIAJE ================")
            print(f"Distancia en Kilómetros : {distancia_km:.2f} km")
            print(f"Distancia en Millas     : {distancia_millas:.2f} mi")
            print(f"Duración estimada       : {horas} horas con {minutos} minutos")
            print("====================================================")
            
            # Narrativa del viaje (Instrucciones de ruta paso a paso)
            print("\n📜 NARRATIVA DEL VIAJE:")
            for paso in ruta["instructions"]:
                texto = paso["text"]
                dist_paso = paso["distance"] / 1000
                print(f"- {texto} ({dist_paso:.2f} km)")
        else:
            print("No se pudo calcular la ruta entre estos puntos.")

if __name__ == "__main__":
    main()