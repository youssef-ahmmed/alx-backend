#!/usr/bin/env python3
"""Infer appropriate time zone"""
from typing import Dict, Union

from flask import Flask, request, render_template, g
from flask_babel import Babel, format_datetime
import pytz
from datetime import datetime as dt


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
    """Get locale from request"""
    url_locale = request.args.get('locale', '')
    if url_locale and url_locale in Config.LANGUAGES:
        return url_locale

    if g.user and g.user.get('locale') in Config.LANGUAGES:
        return g.user.get('locale')

    header_locale = request.headers.get('locale', '')
    if header_locale and header_locale in Config.LANGUAGES:
        return header_locale

    return request.accept_languages.best_match(app.config['LANGUAGES'])


@babel.timezoneselector
def get_timezone() -> str:
    """Get timezone from request"""
    timezone = request.args.get('timezone')
    if not timezone and g.user:
        timezone = g.user.get('timezone')
    try:
        return pytz.timezone(timezone).zone
    except pytz.exceptions.UnknownTimeZoneError:
        return Config.BABEL_DEFAULT_TIMEZONE


@app.route('/', strict_slashes=False)
def index() -> str:
    """Default route"""
    username = g.user.get('name') if g.user else None
    current_time = format_datetime()
    return render_template('index.html',
                           username=username, current_time=current_time)


if __name__ == '__main__':
    app.run()
