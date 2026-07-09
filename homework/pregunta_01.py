"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel


def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.


    """
"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""
import pandas as pd
import re

# pylint: disable=import-outside-toplevel

def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.
    """
    #leer el archivo
    with open('files/input/clusters_report.txt', 'r') as file:
        data_text = file.read()
    # Pre-procesamiento de los datos para la carga
    lines = [line.strip() for line in data_text.strip().split('\n')]
    # Eliminar líneas vacías y el separador '---'
    lines = [line for line in lines if line and not line.startswith('-')]

    data = []
    current_cluster = {}

    # Empezar la iteración después de las dos líneas de encabezado (líneas 0 y 1)
    for line in lines[2:]:
        # Identificar el inicio de un nuevo registro (línea que empieza con un dígito)
        if line and line[0].isdigit():
            # Finalizar el cluster anterior antes de empezar uno nuevo
            if current_cluster:
                current_cluster['Principales palabras clave'] = ' '.join(current_cluster['Principales palabras clave'].split())
                data.append(current_cluster)

            # Usar regex para extraer las primeras 3 columnas (Cluster, Cantidad, Porcentaje)
            match = re.match(r'(\d+)\s+(\d+)\s+([\d, ]+ %)\s*(.*)', line)
            
            if match:
                cluster, count, percentage, keywords_start = match.groups()
                
                current_cluster = {
                    'Cluster': int(cluster),
                    'Cantidad de palabras clave': int(count),
                    'Porcentaje de palabras clave': percentage.strip(),
                    'Principales palabras clave': keywords_start.strip()
                }
            
        elif current_cluster:
            current_cluster['Principales palabras clave'] += ' ' + line.strip()

    # Agregar el último cluster después de terminar el bucle
    if current_cluster:
        current_cluster['Principales palabras clave'] = ' '.join(current_cluster['Principales palabras clave'].split())
        data.append(current_cluster)

    df = pd.DataFrame(data)
    
    df.columns = [
        'cluster', 
        'cantidad_de_palabras_clave', 
        'porcentaje_de_palabras_clave', 
        'principales_palabras_clave'
    ]

    # Reemplazar la coma decimal (,) por el punto decimal (.)
    df['porcentaje_de_palabras_clave'] = df['porcentaje_de_palabras_clave'].str.replace(',', '.', regex=False)
    
    # Quitar el símbolo de porcentaje (%) y cualquier espacio en blanco
    df['porcentaje_de_palabras_clave'] = df['porcentaje_de_palabras_clave'].str.replace('%', '', regex=False).str.strip()

    df['porcentaje_de_palabras_clave'] = df['porcentaje_de_palabras_clave'].astype(float)

    # Normalizar las palabras clave (separadas por coma y un solo espacio)
    def normalizar_palabras_clave(texto):
        # Reemplazar múltiples espacios/saltos de línea por un solo espacio y limpiar
        texto = re.sub(r'\s+', ' ', texto).strip()
        # Asegurar que todas las comas estén seguidas por un único espacio (", ")
        texto = re.sub(r',\s*', ', ', texto)
        # Eliminar el espacio extra al final si la lista termina en ", "
        return texto.strip()

    df['principales_palabras_clave'] = df['principales_palabras_clave'].apply(normalizar_palabras_clave)
    df['principales_palabras_clave'] = df['principales_palabras_clave'].str.rstrip(' .')

    return df