from flask import Flask, render_template, request
from flask_babel import Babel

app = Flask(__name__)
babel = Babel(app)

# Configuración de los idiomas
app.config['BABEL_DEFAULT_LOCALE'] = 'es'
app.config['BABEL_SUPPORTED_LOCALES'] = ['es', 'ca']

# Función para determinar el idioma según la preferencia del usuario
@babel.localeselector
def get_locale():
    return request.args.get('lang', 'es')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
