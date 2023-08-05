
# Stackify Python APM

## Installation Guide

### Django Setup

1. Install **Stackify Linux Agent**.

2. Check that your setup meets our system requirements.

    - Python Versions 3.6 - 3.7
    - Django Versions 1.7 - 2.x

3. Install the Stackify Python APM agent using **pip**:
    ```
    $ pip install stackify-python-apm
    ```
    You may install your stackify-python-apm by adding it to your project's `requirements.txt` file.

4. Add `stackifyapm.contrib.django` to `INSTALLED_APPS` in your `settings.py`:
    ```python
    INSTALLED_APPS = ( # ... 'stackifyapm.contrib.django', )
    ```
5. Add our tracing middleware to `MIDDLEWARE` in your `settings.py`:
    ```python
    MIDDLEWARE = ( 'stackifyapm.contrib.django.middleware.TracingMiddleware', # ... )
    ```

6. Customize **Application Name** and **Environment** configuration in your `settings.py`:
    ```python
    APPLICATION_NAME = 'Python Application'
    ENVIRONMENT = 'Production'
    ```

### Flask Setup

1. Install **Stackify Linux Agent**.

2. Check that your setup meets our system requirements.

    - Python Versions 3.6 - 3.7
    - Flask Versions 0.7 - 1.0

3. Install the Stackify Python APM agent using **pip**:

    ```
    $ pip install stackify-python-apm
    ```

    You may install your stackify-python-apm by adding it to your project's `requirements.txt` file.

4. Update and insert the apm settings to your application:

    ```python
    from stackifyapm.contrib.flask import StackifyAPM

    app = Flask(...)
    StackifyAPM(app)
    ```

5. Customize **Application Name** and **Environment** configuration:
    ```python
    app.config['APPLICATION_NAME'] = 'Python Application'
    app.config['ENVIRONMENT'] = 'Production'

    StackifyAPM(app)
    ```
