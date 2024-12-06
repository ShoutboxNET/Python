"""Pytest configuration file"""

import os
import pytest
from unittest.mock import patch

@pytest.fixture(autouse=True)
def mock_env_vars():
    """Mock environment variables for testing"""
    with patch.dict(os.environ, {
        'SHOUTBOX_API_KEY': 'test-key',
        'SHOUTBOX_FROM': 'test@example.com',
        'SHOUTBOX_TO': 'recipient@example.com'
    }):
        yield

@pytest.fixture
def api_client():
    """Create a test API client"""
    from shoutbox import ShoutboxClient
    return ShoutboxClient(api_key='test-key')

@pytest.fixture
def smtp_client():
    """Create a test SMTP client"""
    from shoutbox import SMTPClient
    return SMTPClient(api_key='test-key')

@pytest.fixture
def sample_email():
    """Create a sample email for testing"""
    from shoutbox import Email
    return Email(
        from_email="sender@example.com",
        to="recipient@example.com",
        subject="Test Email",
        html="<h1>Test</h1>"
    )

@pytest.fixture
def sample_attachment():
    """Create a sample attachment for testing"""
    from shoutbox import Attachment
    return Attachment(
        filename="test.txt",
        content=b"test content",
        content_type="text/plain"
    )

@pytest.fixture
def sample_email_with_attachment(sample_email, sample_attachment):
    """Create a sample email with attachment for testing"""
    sample_email.attachments = [sample_attachment]
    return sample_email
