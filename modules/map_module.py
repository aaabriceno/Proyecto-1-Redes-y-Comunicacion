#Código que genera mapas interactivos con las rutas de traceroute.
#Generaremos un mapa OPEN STREET MAPS
#Usamos la libreria folium para generar el mapa

from pathlib import Path
from typing import List,Tuple,Dict,Optional
import folium
from folium.plugins import AntPath, MarkerCluster

def ventana_html(idx:int, meta:Dict) -> str:
    ip = meta.get("ip","N/A")
    ciudad = meta.get("city") or "-"
    region = meta.get("region") or "-"
    pais = meta.get("country") or "-"
    isp = meta.get("isp") or "-"
    asn = meta.get("as") or "-"
    asname = meta.get("asname") or "-"
    rtt = meta.get("rtt_ms")
    rtt_txt = f"{rtt} ms" if rtt is not None else "-"
    lat = meta.get("lat")
    lon = meta.get("lon")
    coord_txt = f"{lat}, {lon}" if lat is not None and lon is not None else "-"
    return (f"<b>Hop {idx}</b><br>"
            f"<b>IP:</b> {ip}<br>"
            f"<b>Ubicación:</b> {ciudad}, {region}, {pais}<br>"
            f"<b>ISP:</b> {isp}<br>"
            f"<b>ASN:</b> {asn} ({asname})<br>"
            f"<b>RTT:</b> {rtt_txt}<br>"
            f"<b>Coord:</b> {coord_txt}")
    
def crear_tabla_resumen_html(coordenadas_con_nulos: List[Optional[Tuple[float,float,Dict]]]) -> str:
    header = """
    <div style="position: fixed; 
                top: 20px; left: 20px; width: 450px; height: 250px; 
                background-color: rgba(255, 255, 255, 0.85);
                border:2px solid grey; border-radius: 8px; 
                z-index:9999; font-size:12px;
                overflow-y: scroll;
                padding: 5px;">
    <b>Resumen de la Ruta</b>
    <table style="width:100%; border-collapse: collapse;">
    <thead>
        <tr>
            <th style="text-align: left; border-bottom: 1px solid black;">Salto</th>
            <th style="text-align: left; border-bottom: 1px solid black;">IP</th>
            <th style="text-align: left; border-bottom: 1px solid black;">Ubicación</th>
        </tr>
    </thead>
    <tbody>
    """
    
    body = ""
    for i, dato in enumerate(coordenadas_con_nulos):
        hop_num = i + 1
        if dato:
            _, _, meta = dato
            ip = meta.get('ip', 'N/A')
            loc = f"{meta.get('city', '-')}, {meta.get('country', '-')}"
            body += f'<tr><td>{hop_num}</td><td>{ip}</td><td>{loc}</td></tr>'
        else:
            # Muestra los saltos no geolocalizados en la tabla para un resumen completo
            body += f'<tr><td>{hop_num}</td><td>*</td><td>No geolocalizado</td></tr>'

    footer = """
    </tbody>
    </table>
    </div>
    """
    return header + body + footer
    
def generar_mapa (coordenadas_con_nulos: List[Optional[Tuple[float,float,Dict]]], nombre_archivo: str) -> None:
    # Filtramos los que no tienen coordenadas pero mantenemos su índice original
    coordenadas_mapeadas = {i: c for i, c in enumerate(coordenadas_con_nulos) if c}
    if not coordenadas_mapeadas:
        return
    
    indices_mapeados = sorted(coordenadas_mapeadas.keys())
    
    # Crear un mapa vacío. Se centrará automáticamente más adelante.
    n = folium.Map(tiles="OpenStreetMap")
    
    # Crear una capa de cluster para los marcadores
    marker_cluster = MarkerCluster().add_to(n)

    # Trazamos líneas punteadas para saltos no geolocalizados
    for i in range(len(indices_mapeados) - 1):
        idx_actual = indices_mapeados[i]
        idx_siguiente = indices_mapeados[i+1]
        
        # Si hay saltos no geolocalizados en medio, la línea es punteada
        if idx_siguiente > idx_actual + 1:
            lat1, lon1, _ = coordenadas_mapeadas[idx_actual]
            lat2, lon2, _ = coordenadas_mapeadas[idx_siguiente]
            folium.PolyLine(
                locations=[(lat1, lon1), (lat2, lon2)], 
                weight=2, 
                opacity=0.8, 
                color="gray",
                dash_array="5, 10"
            ).add_to(n)

    # Creamos la ruta animada (flechas) solo con los puntos geolocalizados
    puntos_ruta = [[c[0], c[1]] for c in coordenadas_mapeadas.values()]
    AntPath(
        locations=puntos_ruta,
        delay=800,
        weight=5,
        color="#0033FF",
        pulse_color="#FFFFFF",
        paused=False,  # La animación no se repite
        reverse=False
    ).add_to(n)


    # marcadores (inicio=verde, intermedios=azul, fin=rojo)
    total_mapeados = len(indices_mapeados)
    for i, idx_original in enumerate(indices_mapeados):
        lat, lon, meta = coordenadas_mapeadas[idx_original]
        hop_num = idx_original + 1
        
        if i == 0:
            icon = folium.Icon(color="green", icon="play")
        elif i == total_mapeados - 1:
            icon = folium.Icon(color="red", icon="flag")
        else:
            icon = folium.Icon(color="blue", icon="info-sign")

        # Añadimos el marcador al CLUSTER, no directamente al mapa
        folium.Marker(
            location=[lat, lon],
            tooltip=f"Salto {hop_num}: {meta.get('ip','')}",
            popup=folium.Popup(ventana_html(hop_num, meta), max_width=300),
            icon=icon
        ).add_to(marker_cluster)

    # Ajustar el zoom y el centro del mapa para que todos los marcadores sean visibles
    puntos_para_ajuste = [[c[0], c[1]] for c in coordenadas_mapeadas.values()]
    n.fit_bounds(puntos_para_ajuste, padding=(20, 20))

    # Añadir tabla de resumen al mapa
    tabla_html = crear_tabla_resumen_html(coordenadas_con_nulos)
    n.get_root().html.add_child(folium.Element(tabla_html))

    out_dir = Path("resultados/mapas")
    out_dir.mkdir(parents=True, exist_ok=True)
    n.save(str(out_dir / nombre_archivo))
