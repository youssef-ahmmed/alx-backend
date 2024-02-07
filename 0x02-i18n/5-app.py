#!/usr/bin/env python3
"""Mock logging in"""
from typing import Dict, Union

from flask import Flask, request, render_template, g
from flask_babel import Babel


class Config:
    """Babel basic configurations"""

    DEBUG = True
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


def get_user() -> Union[Dict, None]:
    """Returns a user dictionary"""
    login_as = request.args.get('login_as')
    return users.get(int(login_as)) if login_as else None


@app.before_request
def before_request() -> None:
    """Set user as a global"""
    g.user = get_user()


@babel.localeselector
def get_locale() -> str:
    """Get locale"""
    locale = request.args.get('locale', '')
    if locale in Config.LANGUAGES:
        return locale

    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/', strict_slashes=False)
def index() -> str:
    """Default route"""
    username = g.user.get('name') if g.user else None
    return render_template('5-index.html', username=username)


if __name__ == '__main__':
    app.run()
