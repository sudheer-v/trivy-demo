"""
Hello world!
"""
from __future__ import annotations  # pylint: disable=import-error

from flask import Flask  # pylint: disable=import-error
app = Flask(__name__)


@app.route('/')
def hello_world():
    """A dummy docstring."""
    return 'Hello, Docker!'
