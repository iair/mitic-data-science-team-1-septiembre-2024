import requests
import pandas as pd

# Función para consumir los datos de la API
def fetch_data_from_api(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        json_data = response.json()
    else:
        raise Exception(f"Error en la API: {response.status_code}")
    
    return json_data

# Función auxiliar para aplanar un JSON anidado
def flatten(x, name=""):
    out = {}
    if isinstance(x, dict):
        for a in x:
            out.update(flatten(x[a], name + a + "_"))
    elif isinstance(x, list):
        i = 0
        for a in x:
            out.update(flatten(a, name + str(i) + "_"))
            i += 1
    else:
        out[name[:-1]] = x
    return out

# Función para aplanar un JSON completo, que recibe la función flatten como parámetro
def flatten_json(nested_json, flatten_function):
    return flatten_function(nested_json)

# Función para preparar los datos y usar flatten_json de forma opcional
def prepare_data(json_data, flatten_function=None):
    if flatten_function:
        flat_data = [flatten_json(entry, flatten_function) for entry in json_data]
    else:
        flat_data = json_data

    df = pd.DataFrame(flat_data)
    
    return df

# Función para preparar los datos (sin aplanado en este caso)
def prepare_weather_data(json_data):
    # Extraemos solo la información relevante (puedes adaptar esto según lo que necesites)
    main_data = json_data['main']
    wind_data = json_data['wind']
    weather_data = json_data['weather'][0]  # Es una lista, tomamos el primer elemento

    # Combinamos en un solo diccionario
    flat_data = {
        'temperature': main_data['temp'],
        'feels_like': main_data['feels_like'],
        'temp_min': main_data['temp_min'],
        'temp_max': main_data['temp_max'],
        'pressure': main_data['pressure'],
        'humidity': main_data['humidity'],
        'wind_speed': wind_data['speed'],
        'wind_deg': wind_data['deg'],
        'weather_main': weather_data['main'],
        'weather_description': weather_data['description']
    }

    # Creamos un DataFrame
    df = pd.DataFrame([flat_data])
    
    return df