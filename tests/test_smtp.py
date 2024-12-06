"""Tests for the Shoutbox SMTP client"""

import os
import pytest
from unittest.mock import patch, Mock, MagicMock

from shoutbox import SMTPClient, Email, EmailAddress, Attachment
from shoutbox.exceptions import ShoutboxError, ValidationError

def test_smtp_client_initialization():
    """Test SMTP client initialization with API key"""
    # Test with direct API key
    client = SMTPClient(api_key="test-key")
    assert client.api_key == "test-key"
    
    # Test with environment variable
    with patch.dict(os.environ, {'SHOUTBOX_API_KEY': 'env-key'}, clear=True):
        client = SMTPClient()
        assert client.api_key == "env-key"
    
    # Test missing API key
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError):
            SMTPClient()

def test_smtp_client_custom_settings():
    """Test SMTP client with custom settings"""
    client = SMTPClient(
        api_key="test-key",
        host="custom.smtp.server",
        port=465,
        use_tls=True,
        timeout=60
    )
    
    assert client.host == "custom.smtp.server"
    assert client.port == 465
    assert client.use_tls is True
    assert client.timeout == 60

@patch('smtplib.SMTP')
def test_send_basic_email(mock_smtp):
    """Test sending a basic email via SMTP"""
    # Setup mock
    mock_smtp_instance = MagicMock()
    mock_smtp.return_value.__enter__.return_value = mock_smtp_instance
    
    client = SMTPClient(api_key="test-key")
    
    email = Email(
        from_email="sender@example.com",
        to="recipient@example.com",
        subject="Test Email",
        html="<h1>Test</h1>"
    )
    
    success = client.send(email)
    assert success is True
    
    # Verify SMTP calls
    mock_smtp_instance.starttls.assert_called_once()
    mock_smtp_instance.login.assert_called_once_with("test-key", "test-key")
    mock_smtp_instance.send_message.assert_called_once()

@patch('smtplib.SMTP')
def test_send_email_with_attachment(mock_smtp):
    """Test sending an email with attachment via SMTP"""
    # Setup mock
    mock_smtp_instance = MagicMock()
    mock_smtp.return_value.__enter__.return_value = mock_smtp_instance
    
    client = SMTPClient(api_key="test-key")
    
    attachment = Attachment(
        filename="test.txt",
        content=b"test content",
        content_type="text/plain"
    )
    
    email = Email(
        from_email="sender@example.com",
        to="recipient@example.com",
        subject="Test Email with Attachment",
        html="<h1>Test</h1>",
        attachments=[attachment]
    )
    
    success = client.send(email)
    assert success is True
    
    # Verify SMTP calls
    mock_smtp_instance.send_message.assert_called_once()
    args = mock_smtp_instance.send_message.call_args[0]
    message = args[0]
    
    # Verify attachment
    assert len(message.get_payload()) > 1  # HTML part + attachment

@patch('smtplib.SMTP')
def test_send_email_with_multiple_recipients(mock_smtp):
    """Test sending an email to multiple recipients via SMTP"""
    # Setup mock
    mock_smtp_instance = MagicMock()
    mock_smtp.return_value.__enter__.return_value = mock_smtp_instance
    
    client = SMTPClient(api_key="test-key")
    
    email = Email(
        from_email="sender@example.com",
        to=[
            EmailAddress("recipient1@example.com", "John Doe"),
            EmailAddress("recipient2@example.com", "Jane Smith")
        ],
        subject="Test Email",
        html="<h1>Test</h1>"
    )
    
    success = client.send(email)
    assert success is True
    
    # Verify SMTP calls
    mock_smtp_instance.send_message.assert_called_once()
    args = mock_smtp_instance.send_message.call_args[0]
    message = args[0]
    
    # Verify recipients
    assert 'recipient1@example.com' in message['To']
    assert 'recipient2@example.com' in message['To']

@patch('smtplib.SMTP')
def test_smtp_error_handling(mock_smtp):
    """Test SMTP error handling"""
    # Setup mock
    mock_smtp_instance = MagicMock()
    mock_smtp.return_value.__enter__.return_value = mock_smtp_instance
    
    client = SMTPClient(api_key="test-key")
    
    email = Email(
        from_email="sender@example.com",
        to="recipient@example.com",
        subject="Test Email",
        html="<h1>Test</h1>"
    )
    
    # Test authentication error
    mock_smtp_instance.login.side_effect = Exception("Auth failed")
    
    with pytest.raises(ShoutboxError):
        client.send(email)
    
    # Test connection error
    mock_smtp.side_effect = Exception("Connection failed")
    
    with pytest.raises(ShoutboxError):
        client.send(email)

def test_context_manager():
    """Test SMTP client as context manager"""
    with SMTPClient(api_key="test-key") as client:
        assert isinstance(client, SMTPClient)
        
        with patch('smtplib.SMTP') as mock_smtp:
            mock_smtp_instance = MagicMock()
            mock_smtp.return_value.__enter__.return_value = mock_smtp_instance
            
            email = Email(
                from_email="sender@example.com",
                to="recipient@example.com",
                subject="Test Email",
                html="<h1>Test</h1>"
            )
            
            success = client.send(email)
            assert success is True
