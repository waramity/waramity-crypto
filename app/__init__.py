from flask import Flask, g, request, redirect, url_for
from flask_babel import Babel
import os
from flask_socketio import SocketIO

from config import Config
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.debug = True  # Enable debug mode
app.config.from_object(Config)

babel = Babel(app)

from app.features.crypto import crypto as crypto_blueprint, socketio as crypto_socket
app.register_blueprint(crypto_blueprint)

crypto_socket.init_app(app)

@babel.localeselector
def get_locale():
    if not g.get('lang_code', None):
        g.lang_code = request.accept_languages.best_match(
            app.config['LANGUAGES']) or app.config['LANGUAGES'][0]
    return g.lang_code

@app.route('/')
def index():
    if not g.get('lang_code', None):
        get_locale()
    return redirect(url_for('main.index'))
