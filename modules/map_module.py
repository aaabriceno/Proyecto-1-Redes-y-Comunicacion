#Código que genera mapas interactivos con las rutas de traceroute.
#Generaremos un mapa OPEN STREET MAPS
#Usamos la libreria folium para generar el mapa

from pathlib import Path
from typing import List,Tuple,Dict
import folium

def ventana_html(idx:int, meta:Dict) -> str:
    ip = meta.get("ip","N/A")
    ciudad = meta.get("ciudad") or "-"
    region = meta.get("region") or "-"
    pais = meta.get("pais") or "-"
    isp = meta.get("isp") or "-"
    return (f"<b>Hop {idx}</b><br>"
            f"<b>IP:</b> {ip}<br>"
            f"<b>Ubicación:</b> {ciudad}, {region}, {pais}<br>"
            f"<b>ISP:</b> {isp}")