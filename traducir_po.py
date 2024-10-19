import polib
from googletrans import Translator
import time

# Cargar el archivo 'messages.pot'
pot_file = polib.pofile('messages.pot')

# Crear el archivo 'messages.po' para catalán
po_file = polib.POFile()

# Crear un traductor usando Google Translate
translator = Translator()

# Función para dividir cadenas largas en múltiples líneas
def format_po_string(text):
    MAX_LINE_LENGTH = 80  # Longitud máxima de una línea en el archivo .po
    lines = []
    while len(text) > MAX_LINE_LENGTH:
        # Encuentra el último espacio dentro del límite de longitud
        split_index = text.rfind(' ', 0, MAX_LINE_LENGTH)
        if split_index == -1:  # Si no hay espacio, usa el límite de longitud
            split_index = MAX_LINE_LENGTH
        lines.append(text[:split_index].strip() + " ")
        text = text[split_index:].strip()
    lines.append(text)  # Añadir la última parte del texto
    return '\n'.join(f'{line}' for line in lines)

# Función para eliminar solo comillas externas
def limpiar_comillas(translation, original):
    # Solo eliminar comillas si aparecen al principio y al final y no están en el original
    if translation.startswith('"') and translation.endswith('"') and not original.startswith('"') and not original.endswith('"'):
        return translation[1:-1]  # Elimina solo las comillas externas
    return translation  # Devuelve sin cambios si las comillas son parte del texto original

# Iterar sobre los textos en español del archivo 'messages.pot'
for entry in pot_file:
    if entry.msgstr == "":  # Solo traducir entradas que no tengan traducción aún
        try:
            # Traducir el texto al catalán
            translation = translator.translate(entry.msgid, src='es', dest='ca').text

            # Limpiar comillas innecesarias
            translation = limpiar_comillas(translation, entry.msgid)

            print(f"Traduciendo: {entry.msgid} -> {translation}")

            # Formatear la traducción para dividirla en múltiples líneas si es necesario
            formatted_translation = format_po_string(translation)

            # Crear una nueva entrada en el archivo 'messages.po' para catalán
            po_entry = polib.POEntry(
                msgid=entry.msgid,
                msgstr=formatted_translation
            )
            po_file.append(po_entry)

            # Pausa para evitar superar el límite de la API
            time.sleep(1)

        except Exception as e:
            print(f"Error al traducir '{entry.msgid}': {e}")
            continue

# Guardar el archivo 'messages.po' actualizado en la carpeta de catalán
po_file.save('translations/ca/LC_MESSAGES/messages.po')
