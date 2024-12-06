"""Tests for the Shoutbox API client"""

import os
import pytest
from unittest.mock import patch, Mock

from shoutbox import ShoutboxClient, Email, EmailAddress, Attachment
from shoutbox.exceptions import ShoutboxError, ValidationError, APIError

def test_client_initialization():
    """Test client initialization with API key"""
    # Test with direct API key
    client = ShoutboxClient(api_key="test-key")
    assert client.api_key == "test-key"
    
    # Test with environment variable
    with patch.dict(os.environ, {'SHOUTBOX_API_KEY': 'env-key'}, clear=True):
        client = ShoutboxClient()
        assert client.api_key == "env-key"
    
    # Test missing API key
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError):
            ShoutboxClient()

def test_send_basic_email():
    """Test sending a basic email"""
    client = ShoutboxClient(api_key="test-key")
    
    email = Email(
        from_email="sender@example.com",
        to="recipient@example.com",
        subject="Test Email",
        html="<h1>Test</h1>"
    )
    
    with patch('requests.Session.post') as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"status": "success"}
        
        response = client.send(email)
        assert response["status"] == "success"
        
        # Verify the request
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        assert kwargs['json'] == email.to_dict()

def test_send_email_with_attachment():
    """Test sending an email with attachment"""
    client = ShoutboxClient(api_key="test-key")
    
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
    
    with patch('requests.Session.post') as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"status": "success"}
        
        response = client.send(email)
        assert response["status"] == "success"
        
        # Verify attachment was included
        args, kwargs = mock_post.call_args
        assert 'attachments' in kwargs['json']

def test_send_email_with_custom_headers():
    """Test sending an email with custom headers"""
    client = ShoutboxClient(api_key="test-key")
    
    email = Email(
        from_email="sender@example.com",
        to="recipient@example.com",
        subject="Test Email with Headers",
        html="<h1>Test</h1>",
        headers={'X-Custom': 'test'}
    )
    
    with patch('requests.Session.post') as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"status": "success"}
        
        response = client.send(email)
        assert response["status"] == "success"
        
        # Verify headers were included
        args, kwargs = mock_post.call_args
        assert kwargs['json']['headers'] == {'X-Custom': 'test'}

def test_api_error_handling():
    """Test API error handling"""
    client = ShoutboxClient(api_key="test-key")
    
    email = Email(
        from_email="sender@example.com",
        to="recipient@example.com",
        subject="Test Email",
        html="<h1>Test</h1>"
    )
    
    with patch('requests.Session.post') as mock_post:
        # Test API error
        mock_post.return_value.status_code = 400
        mock_post.return_value.text = "Bad Request"
        
        with pytest.raises(APIError):
            client.send(email)
        
        # Test connection error
        mock_post.side_effect = Exception("Connection failed")
        
        with pytest.raises(ShoutboxError):
            client.send(email)

def test_context_manager():
    """Test client as context manager"""
    with ShoutboxClient(api_key="test-key") as client:
        assert isinstance(client, ShoutboxClient)
        
        with patch('requests.Session.post') as mock_post:
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {"status": "success"}
            
            email = Email(
                from_email="sender@example.com",
                to="recipient@example.com",
                subject="Test Email",
                html="<h1>Test</h1>"
            )
            
            response = client.send(email)
            assert response["status"] == "success"
