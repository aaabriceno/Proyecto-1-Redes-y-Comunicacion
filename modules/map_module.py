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
    
def generar_mapa (coordenadas: List[Tuple[float,float,Dict]], nombre_archivo: str) -> None:
    if not coordenadas:
        return
    #centro inicial
    lat0, lon0, _ = coordenadas[0]
    n = folium.Map(location=[lat0,lon0], zoom_start=4, tiles="OpenStreetMap")
    
    #trazamos linea
    poly_pts = [[lat, lon] for (lat, lon, _) in coordenadas]
    folium.PolyLine(poly_pts, weight=3, opacity=0.85).add_to(n)

    # marcadores (inicio=verde, intermedios=azul, fin=rojo)
    total = len(coordenadas)
    for idx, (lat, lon, meta) in enumerate(coordenadas, start=1):
        if idx == 1:
            icon = folium.Icon(color="green", icon="play")
        elif idx == total:
            icon = folium.Icon(color="red", icon="flag")
        else:
            icon = folium.Icon(color="blue", icon="circle")

        folium.Marker(
            location=[lat, lon],
            tooltip=f"Hop {idx}: {meta.get('ip','')}",
            popup=folium.Popup(ventana_html(idx, meta), max_width=300),
            icon=icon
        ).add_to(n)

    out_dir = Path("resultados/mapas")
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / nombre_archivo).write_text(n._repr_html_(), encoding="utf-8")
    # alternativo (más “limpio”): m.save(str(out_dir / nombre_archivo))