Framework Integration
===================

Flask Integration
---------------

.. code-block:: python

   from flask import Flask
   from shoutbox import ShoutboxClient, Email
   from functools import wraps

   app = Flask(__name__)

   def with_shoutbox(f):
       @wraps(f)
       def decorated_function(*args, **kwargs):
           with ShoutboxClient() as client:
               return f(client, *args, **kwargs)
       return decorated_function

Django Integration
----------------

Add the following to your Django settings:

.. code-block:: python

   EMAIL_BACKEND = 'shoutbox.django.ShoutboxEmailBackend'
   SHOUTBOX_API_KEY = 'your-api-key'
