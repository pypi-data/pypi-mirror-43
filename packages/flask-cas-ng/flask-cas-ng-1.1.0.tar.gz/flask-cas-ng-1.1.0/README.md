flask-cas-ng
=========

[![Join the chat at https://gitter.im/cameronbwhite/Flask-CAS](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/cameronbwhite/Flask-CAS?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

[![Build Status](https://travis-ci.org/MasterRoshan/flask-cas-ng.png?branch=master)](https://travis-ci.org/MasterRoshan/flask-cas-ng)

flas-cas-ng is a maintenance fork of https://github.com/cameronbwhite/Flask-CAS

flask-cas-ng is a Flask extension which makes it easy to
authenticate with a CAS Server (v2.0+).

## What is CAS? ##

The Central Authentication Service (CAS) is a single sign-on 
protocol for the web. Its purpose is to permit a user to access 
multiple applications while providing their credentials (such as 
userid and password) only once. It also allows web applications 
to authenticate users without gaining access to a user's security 
credentials, such as a password. The name CAS also refers to a 
software package that implements this protocol. 

http://jasig.github.io/cas

## Demo ##

Want to see it in action? Here is a live demo that lets you 
authenticate against your favorite CAS Server!

http://flask-cas-extension-demo.cameronbwhite.com/

## Installation ##

### PyPI ###

flask-cas-ng is available on PyPI! You can install it with pip.

```sh
pip install flask-cas-ng
```

### Manual ###

If you want to do it the hard way you can clone the repository and
install flask-cas-ng in a virtualenv. 

1. Clone it `git clone git@github.com:MasterRoshan/Flask-CAS.git`
2. Enter it `cd flask-cas-ng`
3. Create a virtualenv and enter it (Optional) `virtualenv venv && source venv/bin/activate`
4. Install it `python setup.py install`

## Instructions ##

Before using flask-cas-ng you will need to specify a `secret_key` for your
app. This is used by the underlying Flask-Session dependency, so ensure
it is secure (random and long). Output from /dev/urandom is a good 
source for this value, or you can hash a non-predictable string.

After flask-cas-ng is installed you will be able to import the `flask_cas`
packages. There is only one thing you care about inside the package
which is the `CAS` class.

```python
from flask_cas import CAS
```

There are two ways to use the `CAS` class.

1. Add the application object at construction time

```python
app = Flask(__name__)
app.secret_key = 'something long and unique and random'
CAS(app)
```

2. Or initialize the application with `CAS.init_app`

```python
cas = CAS()
app = Flask(__name__)
app.secret_key = 'something long and unique and random'
cas.init_app(app)
```

The `CAS` class will add two routes `/login/` and `/logout/`. You can
prefix these routes if you pass a second argument to the `CAS`
constructor or `init_app` depending on the method you choose.

The `/login/` route will redirect the user to the CAS specified by the
`CAS_SERVER` configuration value. If login is successful the user will
be redirect to the endpoint specified by the `CAS_AFTER_LOGIN`
configuration value, and the logged in user's `username` will be store 
in the session under the key specified by the `CAS_USERNAME_SESSION_KEY` 
configuration value. If `attributes` are available, they will be stored 
in the session under the key specified by the 
`CAS_ATTRIBUTES_SESSION_KEY`

The `/logout/` route will redirect the user to the CAS logout page and
the `username` and `attributes` will be removed from the session.

For convenience you can use the `cas.login` and `cas.logout`
functions to redirect users to the login and logout pages. 

```python
from flask_cas import login
from flask_cas import logout
```

If you would like to require that a user is logged in before continuing
you may use the `cas.login_required` method.

```python
from flask_cas import login_required

app.route('/foo')
@login_required
def foo():
    pass
```

### Configuration ###

#### Required Configs ####

|Key             | Description                              | Example              |
|----------------|------------------------------------------|----------------------|
|secret_key      | Unique secret key for Flask-Session      | 'something random'   |
|CAS_SERVER      | URL of CAS                               | 'http://sso.pdx.edu' |  
|CAS_AFTER_LOGIN | Endpoint to go to after successful login | 'root'               |

#### Optional Configs ####

|Key                        | Default               |
|---------------------------|-----------------------|
|CAS_TOKEN_SESSION_KEY      | _CAS_TOKEN            |
|CAS_USERNAME_SESSION_KEY   | CAS_USERNAME          |
|CAS_ATTRIBUTES_SESSION_KEY | CAS_ATTRIBUTES        |
|CAS_LOGIN_ROUTE            | '/cas'                |
|CAS_LOGOUT_ROUTE           | '/cas/logout'         |
|CAS_VALIDATE_ROUTE         | '/cas/serviceValidate'|
|CAS_AFTER_LOGOUT           | None                  |

## Example ##

```python
import flask
from flask import Flask
from flask_cas import CAS
from flask_cas import login_required

app = Flask(__name__)
cas = CAS(app, '/cas')
app.secret_key = 'something long and unique and random'
app.config['CAS_SERVER'] = 'https://sso.pdx.edu' 
app.config['CAS_AFTER_LOGIN'] = 'route_root'

@app.route('/')
@login_required
def route_root():
    return flask.render_template(
        'layout.html',
        username = cas.username,
        display_name = cas.attributes['cas:displayName']
    )
```
