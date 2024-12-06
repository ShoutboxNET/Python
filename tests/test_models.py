"""Tests for the Shoutbox models"""

import os
import pytest
from base64 import b64encode

from shoutbox.models import Email, EmailAddress, Attachment
from shoutbox.exceptions import ValidationError

def test_email_address_validation():
    """Test email address validation"""
    # Valid email addresses
    from_email = os.getenv('SHOUTBOX_FROM')
    to_email = os.getenv('SHOUTBOX_TO')
    
    assert EmailAddress(from_email).email == from_email
    assert EmailAddress(to_email).email == to_email
    assert EmailAddress(from_email, "Test User").name == "Test User"
    assert EmailAddress(f"Test User <{from_email}>").name == "Test User"
    assert EmailAddress(f"Test User <{from_email}>").email == from_email
    
    # Invalid email addresses
    with pytest.raises(ValidationError):
        EmailAddress("not-an-email")
    with pytest.raises(ValidationError):
        EmailAddress("missing@domain")
    with pytest.raises(ValidationError):
        EmailAddress("@missing-local.com")

def test_email_address_string_representation():
    """Test email address string representation"""
    from_email = os.getenv('SHOUTBOX_FROM')
    
    # Without name
    addr = EmailAddress(from_email)
    assert str(addr) == from_email
    
    # With name
    addr = EmailAddress(from_email, "Test User")
    assert str(addr) == f"Test User <{from_email}>"
    
    # From formatted string
    addr = EmailAddress(f"Test User <{from_email}>")
    assert str(addr) == f"Test User <{from_email}>"

def test_attachment_creation():
    """Test attachment creation and serialization"""
    content = b"test content"
    attachment = Attachment(
        filename="test.txt",
        content=content,
        content_type="text/plain"
    )
    
    # Test properties
    assert attachment.filename == "test.txt"
    assert attachment.content == content
    assert attachment.content_type == "text/plain"
    
    # Test serialization
    data = attachment.to_dict()
    assert data['filename'] == "test.txt"
    assert data['content'] == b64encode(content).decode()

def test_email_creation():
    """Test email creation and validation"""
    from_email = os.getenv('SHOUTBOX_FROM')
    to_email = os.getenv('SHOUTBOX_TO')
    
    # Basic email
    email = Email(
        from_email=from_email,
        to=to_email,
        subject="Test",
        html="<h1>Test</h1>"
    )
    
    assert isinstance(email.from_email, EmailAddress)
    assert isinstance(email.to[0], EmailAddress)
    assert email.subject == "Test"
    assert email.html == "<h1>Test</h1>"
    
    # Test serialization
    data = email.to_dict()
    assert data['from'] == from_email
    assert data['to'] == [to_email]
    
    # Email with multiple recipients
    to_addresses = [addr.strip() for addr in to_email.split(',')]
    email = Email(
        from_email=from_email,
        to=to_addresses,
        subject="Test",
        html="<h1>Test</h1>"
    )
    
    assert len(email.to) == len(to_addresses)
    assert all(isinstance(addr, EmailAddress) for addr in email.to)
    
    # Test serialization
    data = email.to_dict()
    assert data['from'] == from_email
    assert data['to'] == to_addresses

def test_email_with_attachments():
    """Test email with attachments"""
    from_email = os.getenv('SHOUTBOX_FROM')
    to_email = os.getenv('SHOUTBOX_TO')
    
    attachment = Attachment(
        filename="test.txt",
        content=b"test content",
        content_type="text/plain"
    )
    
    email = Email(
        from_email=from_email,
        to=to_email,
        subject="Test with attachment",
        html="<h1>Test</h1>",
        attachments=[attachment]
    )
    
    # Test serialization
    data = email.to_dict()
    assert data['from'] == from_email
    assert data['to'] == [to_email]
    assert 'attachments' in data
    assert len(data['attachments']) == 1
    assert data['attachments'][0]['filename'] == "test.txt"

def test_email_with_headers():
    """Test email with custom headers"""
    from_email = os.getenv('SHOUTBOX_FROM')
    to_email = os.getenv('SHOUTBOX_TO')
    
    email = Email(
        from_email=from_email,
        to=to_email,
        subject="Test with headers",
        html="<h1>Test</h1>",
        headers={
            'X-Custom': 'test',
            'X-Priority': '1'
        }
    )
    
    # Test serialization
    data = email.to_dict()
    assert data['from'] == from_email
    assert data['to'] == [to_email]
    assert 'headers' in data
    assert data['headers']['X-Custom'] == 'test'
    assert data['headers']['X-Priority'] == '1'

def test_email_with_reply_to():
    """Test email with reply-to address"""
    from_email = os.getenv('SHOUTBOX_FROM')
    to_email = os.getenv('SHOUTBOX_TO')
    
    email = Email(
        from_email=from_email,
        to=to_email,
        subject="Test with reply-to",
        html="<h1>Test</h1>",
        reply_to=from_email  # Use from_email as reply-to for testing
    )
    
    assert isinstance(email.reply_to, EmailAddress)
    
    # Test serialization
    data = email.to_dict()
    assert data['from'] == from_email
    assert data['to'] == [to_email]
    assert data['reply_to'] == from_email

def test_email_address_conversion():
    """Test various forms of email address input"""
    from_email = os.getenv('SHOUTBOX_FROM')
    to_email = os.getenv('SHOUTBOX_TO')
    
    # String email
    email = Email(
        from_email=from_email,
        to=to_email,
        subject="Test",
        html="<h1>Test</h1>"
    )
    assert isinstance(email.from_email, EmailAddress)
    
    # Test serialization
    data = email.to_dict()
    assert data['from'] == from_email
    assert data['to'] == [to_email]
    
    # EmailAddress object
    email = Email(
        from_email=EmailAddress(from_email, "Sender"),
        to=EmailAddress(to_email, "Recipient"),
        subject="Test",
        html="<h1>Test</h1>"
    )
    assert email.from_email.name == "Sender"
    
    # Test serialization
    data = email.to_dict()
    assert data['from'] == from_email
    assert data['to'] == [to_email]
    assert data['name'] == "Sender"
    
    # Mixed list of strings and EmailAddress objects
    to_addresses = [addr.strip() for addr in to_email.split(',')]
    email = Email(
        from_email=from_email,
        to=[
            to_addresses[0],
            EmailAddress(to_addresses[0], "Recipient 2")
        ],
        subject="Test",
        html="<h1>Test</h1>"
    )
    assert len(email.to) == 2
    assert all(isinstance(addr, EmailAddress) for addr in email.to)
    
    # Test serialization
    data = email.to_dict()
    assert data['from'] == from_email
    assert len(data['to']) == 2
    assert all(isinstance(addr, str) for addr in data['to'])
