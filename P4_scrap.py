import requests
from bs4 import BeautifulSoup

url = "https://www.eluniversal.com.mx/nacion/en-que-consiste-y-que-propone-la-reforma-judicial-propuesta-por-amlo/"

# Cabeceras para simular una solicitud real
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Realizamos la solicitud GET a la página
response = requests.get(url, headers=headers)

# Verificamos si la solicitud fue exitosa (código 200)
if response.status_code == 200:
    # Analizamos el contenido de la página con BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Abrimos el archivo en modo 'append' para no sobreescribir
    with open("C:/Users/rbece/Documents/iaP/TrabajosIA/P4_scrap_info.txt", "a", encoding="utf-8") as file:
        # Extraemos todos los títulos (por ejemplo, h1, h2, h3)
        for element in soup.find_all(['h1', 'h2', 'h3', 'p']):
            file.write(f"{element.get_text().strip()}\n")

        file.write("\n" + "="*50 + "\n")  # Separador entre ejecuciones del script
    print("Datos guardados exitosamente.")
else:
    print(f"Error al acceder a la página, código de estado: {response.status_code}")
