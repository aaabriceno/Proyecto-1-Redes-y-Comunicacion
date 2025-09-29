#Convierte las direcciones IP en coordenadas geográficas (latitud y longitud, INFO_DICT).
#Geolocalizacion de IPs con cacche local  (ip-api.com)

import json
import ipaddress
from pathlib import Path
from typing import Optional, Tuple, Dict
import requests

archivo_cache = Path("resultados/cache_ipgeo.json")
API_URL = "http://ip-api.com/json/{ip}?fields=status,country,regionName,city,lat,lon,isp,query,message"

def cargar_cache()->Dict:
    if archivo_cache:
        try:
            return json.loads(archivo_cache.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}

def guardar_cache(cache: Dict) -> None:
    archivo_cache.parent.mkdir(parents=True, exist_ok= True)
    archivo_cache.write_text(json.dumps(cache,ensure_ascii=False, indent=2),encoding="utf-8")

def es_ipv4_publica(ip: str) -> bool:
    try:
        objeto = ipaddress.ip_address(ip)
        return objeto.version == 4 and not (objeto.is_private or objeto.is_loopback or objeto.is_reserved
                                or objeto.is_multicast or objeto.is_link_local)
    except ValueError:
        return False

def obtener_coordenadas(ip:str) -> Optional[Tuple[float, float, Dict]]:
    if not es_ipv4_publica(ip):
        return None
    cache = cargar_cache()
    if ip in cache and "lat" in cache[ip] and "lon" in cache[ip]:
        d = cache[ip]
        return d["lat"],d["lon"], d

    try:
        r = requests.get(API_URL.format(ip = ip,tiempo_espera2 = 8))
        data = r.json
    except Exception:
        return None
    
    if data.get("status") != "success":
        return None
    
    informacion = {
        "ip": data.get("query"),
        "pais": data.get("country"),
        "region": data.get("regionName"),
        "ciudad": data.get("city"),
        "isp": data.get("isp"),
        "lat": data.get("lat"),
        "lon": data.get("lon"),
    }
    
    cache[ip] = informacion
    guardar_cache(cache)
    
    return informacion["lat"],informacion["lon"], informacion