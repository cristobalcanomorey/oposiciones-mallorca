from flask import Flask, render_template, request
from flask_babel import Babel, _

app = Flask(__name__)

# Configuración de los idiomas
app.config['BABEL_DEFAULT_LOCALE'] = 'es'
app.config['BABEL_TRANSLATION_DIRECTORIES'] = '../translations'

# Inicialización de Babel
babel = Babel(app)

# Función para seleccionar el idioma según la URL
def get_locale():
    lang = request.args.get('lang')
    print(f'Recibido parámetro de idioma: {lang}')  # Depuración para ver si llega el parámetro
    if lang in ['es', 'ca']:
        print(f'Seleccionado idioma: {lang}')  # Depuración para verificar selección de idioma
        return lang
    return 'es'  # Idioma predeterminado si no se encuentra parámetro

# Registra la función de selección de idioma de manera explícita
babel.init_app(app, locale_selector=get_locale)

@app.route('/')
def index():
    print("Página cargada correctamente")  # Depuración para verificar que la página se carga
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
