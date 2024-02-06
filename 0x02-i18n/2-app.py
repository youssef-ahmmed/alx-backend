#!/usr/bin/env python3
"""Get locale from request"""

from flask import Flask, request, render_template
from flask_babel import Babel

app = Flask(__name__)
babel = Babel(app)


@babel.localeselector
def get_locale():
    """Get locale"""
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/', strict_slashes=False)
def index() -> str:
    """Default route"""
    return render_template('1-index.html')


if __name__ == '__main__':
    app.run()

