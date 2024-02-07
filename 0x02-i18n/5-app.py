#!/usr/bin/env python3
"""Mock logging in"""
from typing import Dict

from flask import Flask, request, render_template, g
from flask_babel import Babel


class Config:
    """Babel basic configurations"""
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


@babel.localeselector
def get_locale() -> str:
    """Get locale"""
    locale = request.args.get('locale', '').strip()
    if locale and locale in Config.LANGUAGES:
        return locale

    return request.accept_languages.best_match(app.config['LANGUAGES'])


@babel.localeselector
def get_user() -> Dict:
    """Returns a user dictionary"""
    login_as = request.args.get('login_as', None)
    return users.get(int(login_as) if login_as else None)


@app.before_request
def before_request() -> None:
    """Set user as a global"""
    user = get_user()
    g.user = user if user else None


@app.route('/', strict_slashes=False)
def index() -> str:
    """Default route"""
    user = g.user.get('name') if g.user else None
    return render_template('5-index.html', user=user)


if __name__ == '__main__':
    app.run(debug=True)
