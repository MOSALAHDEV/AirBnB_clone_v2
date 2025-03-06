#!/usr/bin/python3
""" This script starts a Flask web application. """
from flask import Flask, render_template


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """ This function returns a string """
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """ This function returns a string """
    return 'HBNB!'


@app.route('/c/<string:text>', strict_slashes=False)
def c(text):
    """ This function returns a string """
    return 'C ' + text.replace('_', ' ')


@app.route('/python/<string:text>', strict_slashes=False)
@app.route('/python', defaults={'text': 'is cool'}, strict_slashes=False)
def python(text):
    """ This function returns a string """
    return 'Python ' + text.replace('_', ' ')


@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    """ This function returns a string """
    if isinstance(n, int):
        return '{} is a number'.format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n=None):
    """ This function returns a string """
    if isinstance(n, int):
        return render_template('5-number.html', n=n)


@app.route('/odd_or_even/<int:n>', strict_slashes=False)
def number_odd_or_even(n=None):
    """ This function returns a string """
    if isinstance(n, int):
        return render_template('6-number_odd_or_even.html', n=n, even=(n % 2 == 0))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=None)
