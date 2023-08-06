Flask-pymysql
================

A Hacky fork of Flask-MySQLdb, which uses pymysql.

Unlike Flask-MySQLdb, Flask-pymysql uses pymysql which is a pure python driver.
This is a lot more portable than relying on a C binary which often needs to be compiled.

Quickstart
----------

First, install Flask-pymysql:
    
    $ pip install flask-pymysql
    
Next, add a ``MySQL`` instance to your code:

```python
from flask import Flask
from flask_pymysql import MySQL

app = Flask(__name__)

app.config['MYSQL_USER'] = 'user'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'database'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
def users():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT user, host FROM mysql.user''')
    rv = cur.fetchall()
    return str(rv)

if __name__ == '__main__':
    app.run(debug=True)
```


Why
---
Why would you want to use this extension versus just using pymysql by itself?
The only reason is that the extension was made using Flask's best pratices in relation to resources that need caching on the [app context](http://flask.pocoo.org/docs/0.12/appcontext/#context-usage).
What that means is that the extension will manage creating and teardown the connection to MySQL for you while with if you were just using pymysql you would have to do it yourself.


Resources
---------

- [Documentation](http://flask-pymysql.readthedocs.org/en/latest/)
- [PyPI](https://pypi.python.org/pypi/Flask-pymysql)

ToDo
----
Add config parsing, no need to hard code user access credentials.
