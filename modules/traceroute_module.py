#Manejo y ejecución de traceroute/tracert

def ejecutar_traceroute(destino, so):
    import subprocess
    import re

    #verficar el sistema operativo, para poder usar 
    #la herramienta correspondiente para el SO
    comando = []
    if so == "Windows":
        comando = ["tracert", "-d", destino]
    else:
        comando = ["traceroute", "-n", destino]

    try:
        resultado = subprocess.run(comando, capture_output=True, text=True, check=True)
        salida = resultado.stdout
        # Expresión regular para extraer las IPs
        patron_ip = re.compile(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b")
        ips = patron_ip.findall(salida)
        # Eliminar duplicados manteniendo el orden
        ips_unicas = list(dict.fromkeys(ips))
        return ips_unicas
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el comando: {e}")
        return []
    