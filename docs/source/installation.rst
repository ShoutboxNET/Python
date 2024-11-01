Installation
===========

You can install Shoutbox using pip:

.. code-block:: bash

   pip install shoutbox

Configuration
------------

Set your API key either in your environment variables:

.. code-block:: bash

   export SHOUTBOX_API_KEY='your-api-key'

Or when initializing the client:

.. code-block:: python

   from shoutbox import ShoutboxClient
   
   client = ShoutboxClient(api_key='your-api-key')
