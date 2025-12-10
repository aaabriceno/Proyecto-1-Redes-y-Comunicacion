'''
Programa principal que se encarga de coordinar 
las diferentes funcionalidades del proyecto.
'''
import platform
import json
import requests
import time
from pathlib import Path
from modules.traceroute_module import ejecutar_traceroute
from modules.geolocation_module import obtenerCoordenadas, esIPpublicaIPv4
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

def limpiar_ips_paises(ips_por_pais: dict) -> dict:
    """Filtra IPs duplicadas o no públicas y elimina países vacíos."""
    depurado = {}
    descartadas = 0
    for pais, ips in ips_por_pais.items():
        vistos = set()
        validas = []
        for ip in ips:
            if not esIPpublicaIPv4(ip) or ip in vistos:
                descartadas += 1
                continue
            vistos.add(ip)
            validas.append(ip)
        if validas:
            depurado[pais] = validas
    if descartadas:
        print(f"Se descartaron {descartadas} IPs no válidas o duplicadas del dataset.")
    return depurado

def obtener_ip_publica() -> str:
    """Consulta la IP pública del usuario para añadirla como punto inicial."""
    try:
        r = requests.get("https://api.ipify.org?format=json", timeout=5)
        data = r.json()
        ip = data.get("ip")
        if ip and esIPpublicaIPv4(ip):
            return ip
    except Exception:
        pass
    return ""

def _enmascarar_privada(ip: str) -> str:
    partes = ip.split(".")
    if len(partes) == 4:
        return f"{partes[0]}.{partes[1]}.x.x"
    return ip

def guardar_log_ruta(hops:list, coordenadas:list, destino:str, pais:str) -> None:
    out_dir = Path("resultados/logs")
    out_dir.mkdir(parents=True, exist_ok=True)
    log = {
        "destino_ip": destino,
        "pais_destino": pais,
        "timestamp": int(time.time()),
        "saltos": []
    }
    for hop, coord in zip(hops, coordenadas):
        entrada = {"ip": hop.get("ip"), "rtt_ms": hop.get("rtt_ms")}
        if coord:
            lat, lon, meta = coord
            entrada.update({
                "lat": lat,
                "lon": lon,
                "country": meta.get("country"),
                "region": meta.get("region"),
                "city": meta.get("city"),
                "isp": meta.get("isp"),
                "as": meta.get("as"),
                "asname": meta.get("asname"),
            })
        log["saltos"].append(entrada)
    nombre = f"ruta_{pais}_{destino.replace('.', '_')}.json"
    (out_dir / nombre).write_text(json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8")
    


def main():
    print("MiniProyecto de Redes y Comunicaciones")
    #pais = input("Ingresa la IP Publica o dominio de pais")
    
    #Cargar dataset de IPs de paises
    IPS_PAISES = cargar_ips()
    if not IPS_PAISES:
        return
    IPS_PAISES = limpiar_ips_paises(IPS_PAISES)
    if not IPS_PAISES:
        print("No quedan IPs válidas tras la validación del dataset.")
        return

    #Detectamos el SO
    so = platform.system()
    print(f"Detectando Sistema Operativo:{so}")

    #Elejimos el pais destino
    paises = list(IPS_PAISES.keys())
    print("Países disponibles:")
    for i, pais_nombre in enumerate(paises, 1):
        print(f"{i}. {pais_nombre} ({len(IPS_PAISES[pais_nombre])} IPs)")

    while True:
        try:
            opcion_pais = int(input("Elige el número del país de destino: "))
            if not (1 <= opcion_pais <= len(paises)):
                print("Opción fuera de rango. Intenta de nuevo.")
                continue
            pais = paises[opcion_pais - 1]
            break
        except (ValueError, IndexError):
            print("Debes ingresar un número válido de la lista.")
    
    #Comprobamos si el pais existe en el dataset paises_ips.json
    if pais not in IPS_PAISES:
        print("País no disponible en el dataset.")
        return
    
    #Muestra las IPs disponibles y selecciona una IP de las 10 disponibles
    ips_del_pais = IPS_PAISES[pais]
    print(f"IPS disponibles en {pais}:")
    for i, ip in enumerate(ips_del_pais, start=1):
        print(f"{i}. {ip}")
    
    while True:
        try:
            opcion = int(input(f"Elige el número de la IP (1-{len(ips_del_pais)}): "))
            if opcion < 1 or opcion > len(ips_del_pais):
                print("Opción fuera de rango. Intenta de nuevo.")
                continue
            break
        except ValueError:
            print("Debes ingresar un número válido.")
    
    ip_destino = ips_del_pais[opcion - 1]
    print(f"IP destino seleccionada: {ip_destino}")
        
    #1.- Ejecutar traceroute/tracert
    print(f"Ejecutando traceroute hacia: {ip_destino} ({pais})")
    ips_ruta = ejecutar_traceroute(ip_destino, so)

    if not ips_ruta:
        print("No se pudo obtener la ruta. El traceroute no devolvió ninguna IP.")
        return

    # Aseguramos que la IP de destino esté al final si no fue el último salto
    if ips_ruta and ips_ruta[-1].get("ip") != ip_destino:
        # Si el destino ya está en la ruta, lo movemos al final
        if any(h["ip"] == ip_destino for h in ips_ruta):
            ips_ruta = [h for h in ips_ruta if h["ip"] != ip_destino]
        ips_ruta.append({"ip": ip_destino, "rtt_ms": None})

    # Insertamos la IP pública propia como punto de inicio (si existe)
    mi_ip_publica = obtener_ip_publica()
    if mi_ip_publica and not any(h["ip"] == mi_ip_publica for h in ips_ruta):
        ips_ruta.insert(0, {"ip": mi_ip_publica, "rtt_ms": None})
        print(f"Origen (tu IP pública): {mi_ip_publica}")

    # La ruta ya contiene el punto de partida real (la primera IP pública encontrada)
    print("IPs encontradas en el camino:")
    for hop in ips_ruta:
        ip = hop.get("ip")
        rtt = hop.get("rtt_ms")
        rtt_txt = f" [{rtt} ms]" if rtt is not None else ""
        if esIPpublicaIPv4(ip):
            print(" -", f"{ip}{rtt_txt}")
        else:
            print(" -", f"{_enmascarar_privada(ip)} (privada){rtt_txt}")

    # 2.- Obtener coordenadas de las IPs
    coordenadas = [None] * len(ips_ruta)
    for i, hop in enumerate(ips_ruta):
        ip = hop.get("ip")
        dato = obtenerCoordenadas(ip)
        if dato[0] is not None and dato[1] is not None:
            lat, lon, meta = dato
            meta = meta or {}
            meta["rtt_ms"] = hop.get("rtt_ms")
            coordenadas[i] = (lat, lon, meta) #Se agrega lat, long , info_dict de la IP
    
    # Imprimir resumen en consola
    saltos_geolocalizados = [c for c in coordenadas if c is not None]
    print("\n--- Resumen de la Ruta ---")
    print(f"Saltos totales: {len(ips_ruta)}")
    print(f"Saltos geolocalizados: {len(saltos_geolocalizados)}")
    if len(saltos_geolocalizados) > 0:
        inicio = saltos_geolocalizados[0][2]
        fin = saltos_geolocalizados[-1][2]
        pais_inicio = inicio.get('country', 'N/A')
        pais_dest_geo = fin.get('country', 'N/A')
        print(f"País de inicio (geo): {pais_inicio}")
        print(f"País destino seleccionado: {pais}")
        print(f"País de destino (geo): {pais_dest_geo}")
        if pais_dest_geo != "N/A" and pais_dest_geo.lower() != pais.lower():
            print("⚠️ Advertencia: la geolocalización no coincide con el país seleccionado (puede ser IP de otro país o error de la base de datos).")
    print("--------------------------\n")

    #3.- Generar mapa
    if any(coordenadas):
        nombre_archivo = f"ruta_{pais}_{ip_destino.replace('.', '_')}.html"
        generar_mapa(coordenadas, nombre_archivo)
        guardar_log_ruta(ips_ruta, coordenadas, ip_destino, pais)
        print("Mapa y log generados")
    else:
        print("No se pudo geolocalizar ninguna IP. Mapa no generado.")
        
if __name__ == "__main__":
    main()
