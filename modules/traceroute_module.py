#Manejo y ejecución de traceroute/tracert
#Funciona en windows y en linux
#Devuelve una lista de IPs sin duplicados

import subprocess
import re
import shutil

_IP_REGEX = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")

#Esta funcion verifica si un comando existe en el PATH
def existe(cmd:str) -> bool:
    return shutil.which(cmd) is not None

def ejecutar_traceroute(destino:str, so:str,saltos_maximos:int = 40, tiempo_de_espera: int =120):
    #verficar el sistema operativo, para poder usar 
    #la herramienta correspondiente para el SO
    #comando = []
    if so == "Windows":
        if not existe("tracert"):
            print("No se encontro 'tracert' en el PATH")   
            return []
        comando = ["tracert", "-d","-h",str(saltos_maximos), destino]
    else:
        if not existe("traceroute"):
                print("No se encontro 'traceroute' en el PATH")
                return []
        comando = ["traceroute", "-n","-I","-m",str(saltos_maximos), destino]

    try:
        resultado = subprocess.run(comando, capture_output=True, text=True,
                    timeout=tiempo_de_espera, check=True)
        salida = resultado.stdout or resultado.stderr or ""  
    except subprocess.TimeoutExpired:
        print("Traceroute supero el tiempo de espera")
        return []
    except subprocess.CalledProcessError as e:
        print("--- ERROR: TRACEROUTE FALLÓ ---")
        print(f"El comando devolvió un error. Código de salida: {e.returncode}")
        print("Salida del comando (stdout):")
        print(e.stdout)
        print("Salida de error (stderr):")
        print(e.stderr)
        print("---------------------------------")
        return []
    except Exception as e:
        print(f"Error inesperado: {e}")
        return []
    
    ips_encontradas = []
    # Procesar línea por línea para mantener el orden y filtrar encabezados
    for linea in salida.splitlines():
        # Buscar la IP en las líneas que reportan los saltos
        match = _IP_REGEX.search(linea)
        if match and "Traza a la dirección" not in linea and "Traza completa" not in linea:
            ips_encontradas.append(match.group(0))

    # Quitar duplicados conservando el orden
    seen, saltos = set(), []
    for ip in ips_encontradas:
        if ip not in seen:
            seen.add(ip)
            saltos.append(ip)
    return saltos
