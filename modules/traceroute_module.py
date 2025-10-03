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

def ejecutar_traceroute(destino:str, so:str,saltos_maximos:int = 30, tiempo_de_espera: int = 60):
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
        print(f"Error ejecutando traceroute: {e}")
        return []
    except Exception as e:
        print(f"Error inesperado: {e}")
        return []
    
    ips = _IP_REGEX.findall(salida)
    # Quitar duplicados conservando el orden
    seen, saltos = set(), []
    for ip in ips:
        if ip not in seen:
            seen.add(ip)
            saltos.append(ip)
    return saltos
    