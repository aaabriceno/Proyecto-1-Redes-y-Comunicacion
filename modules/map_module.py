#Código que genera mapas interactivos con las rutas de traceroute.


# Genera un mapa OSM con los hops como marcadores y la ruta como PolyLine.
from pathlib import Path
from typing import List, Tuple, Dict
import folium

def _popup_html(idx: int, meta: Dict) -> str:
    ip = meta.get("ip", "N/A")
    city = meta.get("city") or "-"
    region = meta.get("region") or "-"
    country = meta.get("country") or "-"
    isp = meta.get("isp") or "-"
    return (f"<b>Hop {idx}</b><br>"
            f"<b>IP:</b> {ip}<br>"
            f"<b>Ubicación:</b> {city}, {region}, {country}<br>"
            f"<b>ISP:</b> {isp}")

def generar_mapa(coordenadas: List[Tuple[float, float, Dict]], nombre_archivo: str) -> None:
    if not coordenadas:
        return

    lat0, lon0, _ = coordenadas[0]
    m = folium.Map(location=[lat0, lon0], zoom_start=4, tiles="OpenStreetMap")

    # Ruta
    poly_pts = [[lat, lon] for (lat, lon, _) in coordenadas]
    folium.PolyLine(poly_pts, weight=3, opacity=0.85).add_to(m)

    # Marcadores (inicio verde, intermedios azules, fin rojo)
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
            popup=folium.Popup(_popup_html(idx, meta), max_width=300),
            icon=icon
        ).add_to(m)

    out_dir = Path("resultados/mapas")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / nombre_archivo
    m.save(str(out_path))
