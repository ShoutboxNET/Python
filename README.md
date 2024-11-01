# Shoutbox

A Python client for the Shoutbox Email API with support for attachments, custom headers, and framework integrations.

## Features

- Simple, intuitive API for sending emails
- Support for attachments and custom headers
- Built-in Flask and Django integrations
- Comprehensive error handling
- Type hints for better IDE support
- Extensive documentation

## Installation

```bash
pip install shoutbox
```

## Quick Start

```python
from shoutbox import ShoutboxClient, Email

# Initialize client
client = ShoutboxClient(api_key='your-api-key')

# Create and send email
email = Email(
    to="recipient@example.com",
    subject="Hello",
    html="<h1>Hello World!</h1>",
    from_email="sender@yourdomain.com"
)

response = client.send(email)
```

## Documentation

Complete documentation is available at [Read the Docs](https://shoutbox.readthedocs.io/).

## Development

1. Clone the repository
2. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```
3. Run tests:
   ```bash
   pytest
   ```
4. Build documentation:
   ```bash
   cd docs
   make html
   ```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
