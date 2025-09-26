import platform
import json
import random
from traceroute_module import ejecutar_traceroute
from geolocation_module import obtener_coordenadas
from map_module import generar_mapa

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
    destino = input("Ingresa la IP Publica o dominio de destino")
    
    #Cargar dataset de IPs de paises
    IPS_PAISES = cargar_ips()
    if not IPS_PAISES:
        return

    print("Países disponibles:", ", ".join(IPS_PAISES.keys()))
    destino = input("Elige un país destino: ")

    if destino not in IPS_PAISES:
        print("País no disponible en el dataset.")
        return
    
    
    #Detectamos el SO
    so = platform.system()
    print("Detectando Sistema Operativo:{so}")
    
    #1.- Ejecutar traceroute/tracert
    print("Ejecutando traceroute hacia:{destino}")
    ips = ejecutar_traceroute(destino,so)
    print ("IPs encontradas en el camino:")
    for ip in ips:
        print(" -", ip)
    
    
    #2.- Obtener coordenas de las IPs
    coordenadas = []
    for ip in ips:
        coordenada = obtener_coordenadas(ip)
        if coordenada:
            coordenadas.append(coordenada)
    
    #3.- Generar mapa
    if coordenadas:
        generar_mapa(coordenadas, "ruta traceroute.html")
        print("Mapa generado")
    else:
        print("Mapa no generado")
        
if __name__ == "__main__":
    main()