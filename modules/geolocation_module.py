#Convierte las direcciones IP en coordenadas geográficas (latitud y longitud).
import json
import ipaddress
from pathlib import Path
from typing import Dict, Tuple, Optional
import requests

CACHE_FILE = Path("/resultados/cache_IPgeo.json")
api_url = "http://ip-api.com/json/{ip}?fields=status,country,regionName,city,lat,lon,isp,query,message"

def cargarCache() -> Dict:
    if CACHE_FILE.exists():
        try:
            return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}

def guardarCache(cache: Dict) -> None:
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    CACHE_FILE.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")

def esIPpublicaIPv4(IP:str) -> bool:
    try:
        ip = ipaddress.ip_address(IP)
        #ignoramos IPs privadas/loopback/reservadas/etc
        return ip.version == 4 and not (ip.is_private or 
                                        ip.is_reserved or 
                                        ip.is_loopback or 
                                        ip.is_multicast or
                                        ip.is_link_local)
    except ValueError:
        return False   
    
def obtenerCoordenadas(ip:str) -> Optional[Tuple[float, float]]:
    if not esIPpublicaIPv4(ip):
        return None

    cache = cargarCache()
    if ip in cache and "lat" in cache[ip] and "lon" in cache[ip]:
        d = cache[ip]
        return d["lat"], d["lon"], d

    try:
        r = requests.get(api_url.format(ip=ip), timeout=8)
        data = r.json()
    except Exception:
        return None

    if data.get("status") != "success":
        return None

    info = {
        "ip": data.get("query"),
        "country": data.get("country"),
        "region": data.get("regionName"),
        "city": data.get("city"),
        "isp": data.get("isp"),
        "lat": data.get("lat"),
        "lon": data.get("lon"),
    }
    cache[ip] = info
    guardarCache(cache)

    return info["lat"], info["lon"], info