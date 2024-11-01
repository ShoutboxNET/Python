"""
Shoutbox Email API Client
~~~~~~~~~~~~~~~~~~~~~~~~

A Python client for the Shoutbox Email API.

Basic usage:

    >>> from shoutbox import ShoutboxClient, Email
    >>> client = ShoutboxClient('your-api-key')
    >>> email = Email(
    ...     to='recipient@example.com',
    ...     subject='Hello',
    ...     html='<h1>Hello World!</h1>'
    ... )
    >>> response = client.send(email)

:copyright: (c) 2024 by Your Name.
:license: MIT, see LICENSE for more details.
"""

from .client import ShoutboxClient
from .models import Email, EmailAddress, Attachment
from .exceptions import ShoutboxError, ValidationError, APIError

__version__ = '0.1.0'

__all__ = [
    'ShoutboxClient',
    'Email',
    'EmailAddress',
    'Attachment',
    'ShoutboxError',
    'ValidationError',
    'APIError',
]
