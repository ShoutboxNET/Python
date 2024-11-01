Quick Start Guide
===============

Basic Usage
----------

Here's a simple example of sending an email:

.. code-block:: python

   from shoutbox import ShoutboxClient, Email
   
   # Create a client
   client = ShoutboxClient()
   
   # Create an email
   email = Email(
       to="recipient@example.com",
       subject="Hello",
       html="<h1>Hello World!</h1>",
       from_email="sender@yourdomain.com"
   )
   
   # Send the email
   response = client.send(email)
