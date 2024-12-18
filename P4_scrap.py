import requests
from bs4 import BeautifulSoup

urls = [
        "https://politica.expansion.mx/congreso/2024/02/06/reforma-amlo-desaparece-siete-organismos-autonomos",
        "https://www.eleconomista.com.mx/politica/Desaparicion-de-organos-autonomos-El-ABC-de-la-reforma-que-impulsa-Morena-20240810-0005.html",
        "https://www.elfinanciero.com.mx/nacional/2024/11/20/adios-a-organismos-autonomos-cuales-pasan-a-secretarias-y-cuales-desaparecen/",
        "https://www.milenio.com/politica/declaran-constitucional-la-desaparicion-de-organos-autonomos-en-mexico",
        "https://laverdadnoticias.com/politica/sheinbaum-confirma-la-desaparicion-de-organismos-autonomos-en-2025-que-significa-para-mexico-20241209",
        "https://www.infobae.com/mexico/2024/08/24/estos-son-los-7-organos-autonomos-que-desaparecen-con-reforma-propuesta-por-amlo-y-las-secretarias-que-absorberan-sus-funciones/",
        "https://cnnespanol.cnn.com/2024/11/13/organismos-autonomos-desapareceran-mexico-orix/",
        "https://www.elimparcial.com/mexico/2024/11/21/camara-de-diputados-aprueba-la-eliminacion-de-siete-organismos-autonomos-de-mexico-que-significa/",
        "https://oem.com.mx/la-prensa/mexico/desaparicion-de-organismos-autonomos-retroceso-de-20-anos-en-la-democracia-especialistas-18495122",
        "https://www.eleconomista.com.mx/politica/dictamen-sobre-desaparicion-inai-ift-y-otros-organos-autonomos-avanza-senado-20241127-735977.html",
        "https://www.elimparcial.com/mexico/2024/11/21/camara-de-diputados-aprueba-la-eliminacion-de-siete-organismos-autonomos-de-mexico-que-significa/",
        "https://imco.org.mx/desaparicion-de-organos-autonomos/",
        "https://www.jornada.com.mx/noticia/2024/11/28/opinion/el-insustituible-papel-de-los-organismos-autonomos-2545",
        "https://www.eleconomista.com.mx/opinion/alternativas-reforma-constitucional-organismos-constitucionalmente-autonomos-especial-agencias-competencia-20240926-727702.html",
        "https://coparmex.org.mx/que-perdemos-con-la-desaparicion-de-los-organismos-autonomos-derechos-transparencia-y-prograso/"

        

]
# Cabeceras para simular una solicitud real
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
for url in urls:
# Realizamos la solicitud GET a la página
    response = requests.get(url, headers=headers)

    # Verificamos si la solicitud fue exitosa (código 200)
    if response.status_code == 200:
        # Analizamos el contenido de la página con BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        for tag in soup.find_all(['nav', 'footer']):
            tag.decompose()

        # Abrimos el archivo en modo 'append' para no sobreescribir
        with open("C:/Users/rbece/Documents/iaP/TrabajosIA/P4_scrap_info.txt", "a", encoding="utf-8") as file:
            
            # Extraemos todos los títulos (por ejemplo, h1, h2, h3)
            for element in soup.find_all(['h1', 'h2', 'h3', 'p', 'li']):
                file.write(f"{element.get_text().strip()}\n")

            file.write("\n" + "="*50 + "\n")  # Separador entre ejecuciones del script
        print("Datos guardados exitosamente.")
        soup=""
    else:
        print(f"Error al acceder a la página, código de estado: {response.status_code}")
