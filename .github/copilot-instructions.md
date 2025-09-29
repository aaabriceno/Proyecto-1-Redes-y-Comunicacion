# Instrucciones para Agentes de IA - Rastreador de Rutas de Red

## Visión General del Proyecto
Este es un proyecto de análisis de redes que rastrea rutas entre países sudamericanos usando traceroute/tracert, geolocaliza las IPs intermedias y visualiza las rutas en mapas interactivos HTML con Folium.

## Arquitectura del Sistema

### Flujo Principal (`main.py`)
1. **Carga de dataset**: Lee `paises_ips.json` con IPs representativas de países sudamericanos
2. **Detección de SO**: Adapta comandos de traceroute según Windows (`tracert`) o Unix (`traceroute`)
3. **Pipeline de procesamiento**: traceroute → geolocalización → visualización en mapa

### Módulos del Sistema (`modules/`)

#### `traceroute_module.py`
- **Patrón clave**: Adapta comandos según SO usando `platform.system()`
- **Comando Windows**: `["tracert", "-d", destino]`
- **Comando Unix**: `["traceroute", "-n", destino]`
- **Extracción de IPs**: Usa regex `r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"`
- **Deduplicación**: `list(dict.fromkeys(ips))` para mantener orden

#### `geolocation_module.py` (INCOMPLETO)
- **API objetivo**: http://ip-api.com/json/ (gratuita)
- **Función esperada**: `obtener_coordenadas(ip)` → dict con lat, lon, país, ciudad, ISP
- **Patrón requerido**: Filtrar IPs privadas (192.168.x.x, 10.x.x.x)

#### `map_module.py` (INCOMPLETO) 
- **Biblioteca**: Folium para mapas HTML interactivos
- **Función esperada**: `generar_mapa(coordenadas, nombre_archivo)`
- **Patrones de visualización**: Marcadores diferenciados (origen/destino/intermedio), líneas rojas conectoras

## Dataset de IPs (`paises_ips.json`)
- **Estructura**: `{"País": ["ip1", "ip2", "ip3"]}`
- **Cobertura**: 14 países sudamericanos + Panamá
- **Uso**: El usuario selecciona país y luego una IP específica (1-10)

## Convenciones del Proyecto

### Manejo de Errores
- Validación de archivo JSON con mensajes específicos
- `subprocess.CalledProcessError` para fallos de traceroute
- Validación de rangos de entrada del usuario

### Nomenclatura de Archivos de Salida
- **Mapas**: `ruta_{pais}_{ip_con_guiones_bajos}.html`
- **Ejemplo**: `ruta_Peru_200_16_6_1.html`

### Interacción con Usuario
- Menús numerados con emojis para claridad visual
- Validación de entrada con manejo de `ValueError`
- Feedback progresivo durante operaciones largas

## Comandos de Desarrollo

```bash
# Instalación de dependencias
pip install requests folium plotly matplotlib pandas

# Ejecución principal
python main.py

# Estructura esperada de salida
# 1. Consola: Resumen de países atravesados y detalles por salto
# 2. HTML: Mapa interactivo en directorio raíz
```

## Patrones de Implementación

### Para `geolocation_module.py`:
- Implementar cache local para evitar consultas repetidas a la API
- Rate limiting para respetar límites de API gratuita
- Retornar `None` para IPs que no se pueden geolocalizar

### Para `map_module.py`:
- Centrar mapa automáticamente basado en coordenadas de la ruta
- Usar `folium.PolyLine()` para líneas conectoras rojas
- PopUps con información detallada: IP, ciudad, país, ISP

### Manejo de Plataformas
- Siempre usar `platform.system()` para detectar SO
- Timeout configurable (actualmente 60s implícito en subprocess)
- Máximo 30 saltos por defecto en traceroute

## Notas de Desarrollo
- `requeriments.txt` está vacío - generar basado en imports del código
- Los módulos de geolocalización y mapas están solo declarados - requieren implementación completa
- El proyecto está orientado a análisis educativo/universitario de redes