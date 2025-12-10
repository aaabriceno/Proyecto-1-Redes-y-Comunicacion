#Manejo y ejecución de traceroute/tracert
#Funciona en windows y en linux
#Devuelve una lista de IPs sin duplicados

import subprocess
import re
import shutil
import ipaddress

_IP_REGEX = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
_RTT_REGEX = re.compile(r"(\d+(?:\.\d+)?)\s*ms")

#Esta funcion verifica si un comando existe en el PATH
def existe(cmd:str) -> bool:
    return shutil.which(cmd) is not None

def _es_publica_ipv4(ip_str: str) -> bool:
    try:
        ip = ipaddress.ip_address(ip_str)
        return ip.version == 4 and ip.is_global
    except ValueError:
        return False

def ejecutar_traceroute(destino:str, so:str,saltos_maximos:int = 40, tiempo_de_espera: int =120):
    #verficar el sistema operativo, para poder usar 
    #la herramienta correspondiente para el SO
    comandos = []
    if so == "Windows":
        if not existe("tracert"):
            print("No se encontro 'tracert' en el PATH")   
            return []
        comandos.append(["tracert", "-d","-h",str(saltos_maximos), destino])
    else:
        if existe("traceroute"):
            # Prioridad: ICMP (-I). Si requiere permisos y falla, probamos UDP.
            comandos.append(["traceroute", "-I", "-n", "-q", "1", "-w", "2", "-m", str(saltos_maximos), destino])
            comandos.append(["traceroute", "-n", "-q", "1", "-w", "2", "-m", str(saltos_maximos), destino])
        if existe("tracepath"):
            comandos.append(["tracepath", "-n", "-m", str(saltos_maximos), destino])
        if not comandos:
            print("No se encontró 'traceroute' ni 'tracepath' en el PATH")
            return []

    salida = ""
    # Probar los comandos en orden hasta que uno funcione
    for comando in comandos:
        try:
            resultado = subprocess.run(comando, capture_output=True, text=True,
                        timeout=tiempo_de_espera, check=True)
            salida = resultado.stdout or resultado.stderr or ""  
            break  # éxito
        except subprocess.TimeoutExpired:
            print("Traceroute supero el tiempo de espera")
            return []
        except subprocess.CalledProcessError as e:
            print("--- ERROR: TRACEROUTE FALLÓ ---")
            print(f"Comando: {' '.join(comando)}")
            print(f"Código de salida: {e.returncode}")
            print("Salida del comando (stdout):")
            print(e.stdout)
            print("Salida de error (stderr):")
            print(e.stderr)
            print("---------------------------------")
            # Intentaremos con el siguiente comando de la lista
            continue
        except Exception as e:
            print(f"Error inesperado con {' '.join(comando)}: {e}")
            continue
    else:
        # Ningún comando funcionó
        return []
    
    ips_encontradas = []
    # Procesar línea por línea para mantener el orden y filtrar encabezados
    for linea in salida.splitlines():
        # Buscar la IP en las líneas que reportan los saltos
        match = _IP_REGEX.search(linea)
        if match and "Traza a la dirección" not in linea and "Traza completa" not in linea:
            ip_encontrada = match.group(0)
            if ip_encontrada == "0.0.0.0":
                continue
            rtt = None
            rtt_match = _RTT_REGEX.search(linea)
            if rtt_match:
                try:
                    rtt = float(rtt_match.group(1))
                except ValueError:
                    rtt = None
            # Incluimos también IPs privadas para mostrar el salto local en consola
            ips_encontradas.append({"ip": ip_encontrada, "rtt_ms": rtt})

    # Quitar duplicados conservando el orden
    seen, saltos = set(), []
    for hop in ips_encontradas:
        ip = hop["ip"]
        if ip not in seen:
            seen.add(ip)
            saltos.append(hop)
    return saltos
