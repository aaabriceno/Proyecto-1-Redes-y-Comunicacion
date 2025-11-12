'''
Programa principal que se encarga de coordinar 
las diferentes funcionalidades del proyecto.
'''
import platform
import json
import random
from modules.traceroute_module import ejecutar_traceroute
from modules.geolocation_module import obtenerCoordenadas
from modules.map_module import generar_mapa

def cargar_ips(nombre_archivo="paises_ips.json"):
    try:
        with open(nombre_archivo, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"No se encontró el archivo {nombre_archivo}.")
        return {}
    except json.JSONDecodeError:
        print("Error al leer el archivo JSON. Verifica el formato.")
        return {}
    


def main():
    print("MiniProyecto de Redes y Comunicaciones")
    #pais = input("Ingresa la IP Publica o dominio de pais")
    
    #Cargar dataset de IPs de paises
    IPS_PAISES = cargar_ips()
    if not IPS_PAISES:
        return

    #Detectamos el SO
    so = platform.system()
    print(f"Detectando Sistema Operativo:{so}")

    #Elejimos el pais destino
    paises = list(IPS_PAISES.keys())
    print("Países disponibles:")
    for i, pais_nombre in enumerate(paises, 1):
        print(f"{i}. {pais_nombre}")

    try:
        opcion_pais = int(input("Elige el número del país de destino: "))
        if not (1 <= opcion_pais <= len(paises)):
            print("Opción fuera de rango.")
            return
        pais = paises[opcion_pais - 1]
    except (ValueError, IndexError):
        print("Debes ingresar un número válido de la lista.")
        return
    
    #Comprobamos si el pais existe en el dataset paises_ips.json
    if pais not in IPS_PAISES:
        print("País no disponible en el dataset.")
        return
    
    #Muestra las IPs disponibles y selecciona una IP de las 10 disponibles
    print(f"IPS disponibles en {pais}:")
    for i, ip in enumerate(IPS_PAISES[pais], start=1):
        print(f"{i}. {ip}")
    
    try:
        opcion = int(input("Elige el número de la IP (1-10): "))
        if opcion < 1 or opcion > len(IPS_PAISES[pais]):
            print("Opción fuera de rango.")
            return
    except ValueError:
        print("Debes ingresar un número válido.")
        return
    
    ip_destino = IPS_PAISES[pais][opcion - 1]
    print(f"IP destino seleccionada: {ip_destino}")
        
    #1.- Ejecutar traceroute/tracert
    print(f"Ejecutando traceroute hacia: {ip_destino} ({pais})")
    ips_ruta = ejecutar_traceroute(ip_destino, so)

    if not ips_ruta:
        print("No se pudo obtener la ruta. El traceroute no devolvió ninguna IP.")
        return

    # Aseguramos que la IP de destino esté al final si no fue el último salto
    if ips_ruta and ips_ruta[-1] != ip_destino:
        # Si el destino ya está en la ruta, lo movemos al final
        if ip_destino in ips_ruta:
            ips_ruta.remove(ip_destino)
        ips_ruta.append(ip_destino)

    # La ruta ya contiene el punto de partida real (la primera IP pública encontrada)
    print("IPs encontradas en el camino:")
    for ip in ips_ruta:
        print(" -", ip)

    # 2.- Obtener coordenadas de las IPs
    coordenadas = [None] * len(ips_ruta)
    for i, ip in enumerate(ips_ruta):
        dato = obtenerCoordenadas(ip)
        if dato[0] is not None and dato[1] is not None:
            coordenadas[i] = dato #Se agrega lat, long , info_dict de la IP
    
    # Imprimir resumen en consola
    saltos_geolocalizados = [c for c in coordenadas if c is not None]
    print("\n--- Resumen de la Ruta ---")
    print(f"Saltos totales: {len(ips_ruta)}")
    print(f"Saltos geolocalizados: {len(saltos_geolocalizados)}")
    if len(saltos_geolocalizados) > 0:
        inicio = saltos_geolocalizados[0][2]
        fin = saltos_geolocalizados[-1][2]
        print(f"País de inicio: {inicio.get('country', 'N/A')}")
        print(f"País de destino: {fin.get('country', 'N/A')}")
    print("--------------------------\n")

    #3.- Generar mapa
    if any(coordenadas):
        nombre_archivo = f"ruta_{pais}_{ip_destino.replace('.', '_')}.html"
        generar_mapa(coordenadas, nombre_archivo)
        print("Mapa generado")
    else:
        print("No se pudo geolocalizar ninguna IP. Mapa no generado.")
        
if __name__ == "__main__":
    main()