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
    print("Países disponibles:", ", ".join(IPS_PAISES.keys()))
    pais = input("Elige un país pais: ")

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
    print(f"Ejecutando traceroute hacia:{ip_destino} ({pais})")
    ips = ejecutar_traceroute(ip_destino,so)
    print ("IPs encontradas en el camino:")
    for ip in ips:
        print(" -", ip)
    
    #2.- Obtener coordenas de las IPs
    coordenadas = []
    for ip in ips:
        dato = obtenerCoordenadas(ip)
        if dato:
            coordenadas.append(dato) #Se agrega lat, long , info_dict de la IP
    
    #3.- Generar mapa
    if coordenadas:
        nombre_archivo = f"ruta_{pais}_{ip_destino.replace('.', '_')}.html"
        generar_mapa(coordenadas, nombre_archivo)
        print("Mapa generado")
    else:
        print("Mapa no generado")
        
if __name__ == "__main__":
    main()