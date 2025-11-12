#Convierte las direcciones IP en coordenadas geográficas (latitud y longitud).
import json
import ipaddress
from pathlib import Path
from typing import Dict, Tuple, Optional
import requests

CACHE_FILE = Path("resultados/cache_IPgeo.json")
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
        # Ignoramos IPs privadas, de loopback, reservadas, etc.
        # Tu profesor mencionó las 10.x.x.x y 127.x.x.x (loopback)
        # ip.is_private cubre: 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16
        return ip.version == 4 and ip.is_global
    except ValueError:
        return False   
    
def obtenerCoordenadas(ip:str) -> Optional[Tuple[float, float, dict]]:
    if not esIPpublicaIPv4(ip):
        return None, None, None

    cache = cargarCache()
    if ip in cache and "lat" in cache[ip] and "lon" in cache[ip]:
        d = cache[ip]
        return d.get("lat"), d.get("lon"), d

    try:
        r = requests.get(api_url.format(ip=ip), timeout=8)
        data = r.json()
    except Exception:
        return None, None, None

    if data.get("status") != "success":
        return None, None, None

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

    return info.get("lat"), info.get("lon"), info