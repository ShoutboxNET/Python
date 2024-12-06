"""Tests for the Shoutbox models"""

import pytest
from base64 import b64encode

from shoutbox.models import Email, EmailAddress, Attachment
from shoutbox.exceptions import ValidationError

def test_email_address_validation():
    """Test email address validation"""
    # Valid email addresses
    assert EmailAddress("test@example.com").email == "test@example.com"
    assert EmailAddress("test@example.com", "Test User").name == "Test User"
    assert EmailAddress("Test User <test@example.com>").name == "Test User"
    assert EmailAddress("Test User <test@example.com>").email == "test@example.com"
    
    # Invalid email addresses
    with pytest.raises(ValidationError):
        EmailAddress("not-an-email")
    with pytest.raises(ValidationError):
        EmailAddress("missing@domain")
    with pytest.raises(ValidationError):
        EmailAddress("@missing-local.com")

def test_email_address_string_representation():
    """Test email address string representation"""
    # Without name
    addr = EmailAddress("test@example.com")
    assert str(addr) == "test@example.com"
    
    # With name
    addr = EmailAddress("test@example.com", "Test User")
    assert str(addr) == "Test User <test@example.com>"
    
    # From formatted string
    addr = EmailAddress("Test User <test@example.com>")
    assert str(addr) == "Test User <test@example.com>"

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
    # Basic email
    email = Email(
        from_email="sender@example.com",
        to="recipient@example.com",
        subject="Test",
        html="<h1>Test</h1>"
    )
    
    assert isinstance(email.from_email, EmailAddress)
    assert isinstance(email.to[0], EmailAddress)
    assert email.subject == "Test"
    assert email.html == "<h1>Test</h1>"
    
    # Email with multiple recipients
    email = Email(
        from_email="sender@example.com",
        to=["recipient1@example.com", "recipient2@example.com"],
        subject="Test",
        html="<h1>Test</h1>"
    )
    
    assert len(email.to) == 2
    assert all(isinstance(addr, EmailAddress) for addr in email.to)

def test_email_with_attachments():
    """Test email with attachments"""
    attachment = Attachment(
        filename="test.txt",
        content=b"test content",
        content_type="text/plain"
    )
    
    email = Email(
        from_email="sender@example.com",
        to="recipient@example.com",
        subject="Test with attachment",
        html="<h1>Test</h1>",
        attachments=[attachment]
    )
    
    # Test serialization
    data = email.to_dict()
    assert 'attachments' in data
    assert len(data['attachments']) == 1
    assert data['attachments'][0]['filename'] == "test.txt"

def test_email_with_headers():
    """Test email with custom headers"""
    email = Email(
        from_email="sender@example.com",
        to="recipient@example.com",
        subject="Test with headers",
        html="<h1>Test</h1>",
        headers={
            'X-Custom': 'test',
            'X-Priority': '1'
        }
    )
    
    # Test serialization
    data = email.to_dict()
    assert 'headers' in data
    assert data['headers']['X-Custom'] == 'test'
    assert data['headers']['X-Priority'] == '1'

def test_email_with_reply_to():
    """Test email with reply-to address"""
    email = Email(
        from_email="sender@example.com",
        to="recipient@example.com",
        subject="Test with reply-to",
        html="<h1>Test</h1>",
        reply_to="reply@example.com"
    )
    
    assert isinstance(email.reply_to, EmailAddress)
    
    # Test serialization
    data = email.to_dict()
    assert 'reply_to' in data
    assert 'reply@example.com' in data['reply_to']

def test_email_address_conversion():
    """Test various forms of email address input"""
    # String email
    email = Email(
        from_email="sender@example.com",
        to="recipient@example.com",
        subject="Test",
        html="<h1>Test</h1>"
    )
    assert isinstance(email.from_email, EmailAddress)
    
    # EmailAddress object
    email = Email(
        from_email=EmailAddress("sender@example.com", "Sender"),
        to=EmailAddress("recipient@example.com", "Recipient"),
        subject="Test",
        html="<h1>Test</h1>"
    )
    assert email.from_email.name == "Sender"
    
    # Mixed list of strings and EmailAddress objects
    email = Email(
        from_email="sender@example.com",
        to=[
            "recipient1@example.com",
            EmailAddress("recipient2@example.com", "Recipient 2")
        ],
        subject="Test",
        html="<h1>Test</h1>"
    )
    assert len(email.to) == 2
    assert all(isinstance(addr, EmailAddress) for addr in email.to)
    assert email.to[1].name == "Recipient 2"
