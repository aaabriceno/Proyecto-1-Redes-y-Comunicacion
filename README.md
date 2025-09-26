# 🌎 Proyecto de Rastreo de Rutas de Red - Sudamérica

Este proyecto tiene el objetivo de poder mostrar que caminos toma una conexión entre países de Sudamérica, visualizando la ruta completa de IPs públicas que sigue una conexión de red.

## 🎯 Objetivos

- Rastrear rutas de red entre direcciones IP públicas de países sudamericanos
- Visualizar geográficamente cada salto de la conexión
- Identificar los países e ISPs por los que pasa la conexión
- Proporcionar una interfaz fácil de usar para análisis de rutas

## 🚀 Funcionalidades

### 1. **Traceroute Avanzado**
- Realiza traceroute hacia IPs de destino
- Captura todas las IPs públicas intermedias
- Filtra IPs privadas automáticamente

### 2. **Geolocalización de IPs**
- Identifica país, ciudad y coordenadas de cada IP
- Obtiene información del ISP y organización
- Utiliza API gratuita de geolocalización (ip-api.com)

### 3. **Visualización Interactiva**
- Genera mapas interactivos HTML con Folium
- Conecta los puntos geográficos con líneas
- Muestra información detallada en popups

### 4. **Base de Datos de IPs Sudamericanas**
Incluye IPs públicas representativas de:
- 🇵🇪 Perú 
- 🇵🇾 Paraguay
- 🇨🇴 Colombia
- 🇦🇷 Argentina
- 🇧🇷 Brasil
- 🇨🇱 Chile
- 🇪🇨 Ecuador
- 🇻🇪 Venezuela
- 🇧🇴 Bolivia
- 🇺🇾 Uruguay
- PA Panama 

## 📋 Requisitos

### Dependencias Python:
```
requests      # Para consultas HTTP a APIs
folium        # Para mapas interactivos
plotly        # Para visualizaciones avanzadas  
socket        # Para validación de IPs
subprocess    # Para ejecutar traceroute
```

### Herramientas del Sistema:
- **Windows**: `tracert` (incluido en el sistema)
- **Linux/macOS**: `traceroute` (puede requerir instalación)

## 🛠️ Instalación

1. **Clonar el repositorio**:
```bash
git clone https://github.com/aaabriceno/Proyecto-1-Redes-y-Comunicacion.git
cd Proyecto-1-Redes-y-Comunicacion
```

2. **Instalar dependencias**:
```bash
pip install requests folium plotly matplotlib pandas
```

3. **Ejecutar el programa**:
```bash
python main.py
```

## 🎮 Uso

### Menú Principal
El programa ofrece un menú interactivo con las siguientes opciones:

1. **🌍 Listar países disponibles**: Muestra todos los países sudamericanos con IPs configuradas
2. **🔍 Rastrear ruta a IP específica**: Permite ingresar cualquier IP para rastrear
3. **🗺️ Rastrear ruta entre países**: Selecciona un país y rastrea hacia sus IPs públicas
4. **🚪 Salir**: Termina el programa

### Ejemplo de Uso
```
🚀 RASTREADOR DE RUTAS DE RED - SUDAMÉRICA
==================================================

📋 MENÚ PRINCIPAL:
1. 🌍 Listar países disponibles
2. 🔍 Rastrear ruta a IP específica  
3. 🗺️ Rastrear ruta entre países
4. 🚪 Salir

➤ Selecciona una opción (1-4): 3

🌎 PAÍSES SUDAMERICANOS DISPONIBLES:
----------------------------------------
 1. Peru         (10 IPs)
 2. Paraguay     (10 IPs) 
 3. Colombia     (10 IPs)
 ...

➤ Selecciona un país de destino: Paraguay

🎯 Rastreando ruta hacia Paraguay (181.120.96.1)...
🔍 Iniciando traceroute hacia 181.120.96.1...
✅ Traceroute completado. Se encontraron 8 saltos públicos.
🌍 Geolocalizando 8 saltos...
```

## 📊 Resultados

### Salida en Consola
- Resumen de países atravesados
- Detalle de cada salto con IP, ciudad, país e ISP
- Número total de saltos

### Mapa Interactivo HTML
- Archivo HTML generado automáticamente
- Marcadores en cada punto de la ruta
- Líneas conectando los puntos geográficamente
- Popups con información detallada de cada salto

### Ejemplo de Salida:
```
================================================================================
📊 RESUMEN DE LA RUTA DE RED  
================================================================================
🌍 Países atravesados: Peru, Brasil, Paraguay
🔗 Total de saltos: 8

📍 Detalle de cada salto:
--------------------------------------------------------------------------------
Salto  1: 200.48.225.130 -> Lima            , Peru           (Telefonica del Peru)
Salto  2: 200.48.225.1   -> Lima            , Peru           (Telefonica del Peru)
Salto  3: 189.38.95.95   -> São Paulo       , Brasil         (Brasil Telecom)
...
```

## 🔧 Características Técnicas

### Algoritmo de Traceroute
- Utiliza comando nativo del sistema (`tracert` en Windows, `traceroute` en Unix)
- Timeout configurable de 60 segundos
- Filtrado automático de IPs privadas (192.168.x.x, 10.x.x.x)
- Máximo de 30 saltos por defecto

### Geolocalización
- API gratuita: http://ip-api.com/json/
- Cache local para evitar consultas repetidas
- Rate limiting para respetar límites de API
- Manejo de errores robusto

### Visualización
- Mapas centrados automáticamente en la ruta
- Marcadores diferenciados por posición (origen, destino, intermedio)
- Coordenadas conectadas con líneas rojas
- Compatible con navegadores web modernos

## ⚠️ Limitaciones

- Requiere acceso a internet para geolocalización
- Algunos routers pueden no responder al traceroute
- La precisión de geolocalización varía según la IP
- API gratuita tiene límites de consultas por minuto

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Puedes:
- Agregar más IPs representativas de países
- Mejorar la precisión de geolocalización
- Implementar nuevas visualizaciones
- Optimizar el rendimiento

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 👨‍💻 Autor

**Anthony Briceño**  
Proyecto universitario - Redes y Comunicación  
Septiembre 2025
