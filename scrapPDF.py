import PyPDF2

ruta_txt = "C:/Users/rbece/Documents/iaP/TrabajosIA/P4_scrap_info.txt"
ruta_pdf = "C:/Users/rbece/Downloads/reforma-integral-al-sistema-de-justicia-en-mexico.pdf"

def agregar_texto_a_txt(pdf_ruta, txt_ruta):
    # Abrir el archivo PDF
    with open(pdf_ruta, 'rb') as archivo_pdf:
        lector_pdf = PyPDF2.PdfReader(archivo_pdf)
        texto = ""

        # Extraer texto de todas las páginas del PDF
        for pagina_numero in range(len(lector_pdf.pages)):
            pagina = lector_pdf.pages[pagina_numero]
            texto += pagina.extract_text() + "\n"  # Añadir un salto de línea entre páginas

    # Abrir el archivo de texto en modo 'append' para agregar contenido sin reemplazar
    with open(txt_ruta, 'a', encoding='utf-8') as archivo_texto:
        archivo_texto.write(texto)

# Ejemplo de uso
agregar_texto_a_txt(ruta_pdf, ruta_txt)