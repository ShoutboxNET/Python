"""
Shoutbox models
~~~~~~~~~~~~~

This module contains the models used by Shoutbox.
"""

import base64
import typing
from dataclasses import dataclass, field
from email.utils import parseaddr
import re

from .exceptions import ValidationError

@dataclass
class EmailAddress:
    email: str
    name: typing.Optional[str] = None

    def __post_init__(self):
        name, addr = parseaddr(self.email)
        if not addr or not self._is_valid_email(addr):
            raise ValidationError(f"Invalid email address: {self.email}")
        self.email = addr
        if not self.name and name:
            self.name = name

    def _is_valid_email(self, email: str) -> bool:
        """Validate email address format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    def __str__(self):
        if self.name:
            return f"{self.name} <{self.email}>"
        return self.email

@dataclass
class Attachment:
    filename: str
    content: bytes
    content_type: typing.Optional[str] = None

    def to_dict(self):
        return {
            'filename': self.filename,
            'content': base64.b64encode(self.content).decode()
        }

@dataclass
class Email:
    to: typing.Union[str, list[str], EmailAddress, list[EmailAddress]]
    subject: str
    html: str
    from_email: typing.Optional[typing.Union[str, EmailAddress]] = None
    reply_to: typing.Optional[typing.Union[str, EmailAddress]] = None
    headers: typing.Optional[dict] = field(default_factory=dict)
    attachments: typing.Optional[list[Attachment]] = field(default_factory=list)

    def __post_init__(self):
        # Convert string emails to EmailAddress objects
        if isinstance(self.to, str):
            self.to = [EmailAddress(self.to)]
        elif isinstance(self.to, list):
            self.to = [EmailAddress(addr) if isinstance(addr, str) else addr for addr in self.to]
        elif isinstance(self.to, EmailAddress):
            self.to = [self.to]

        if isinstance(self.from_email, str):
            self.from_email = EmailAddress(self.from_email)
        
        if isinstance(self.reply_to, str):
            self.reply_to = EmailAddress(self.reply_to)

    def to_dict(self) -> dict:
        payload = {
            'to': ','.join(str(addr) for addr in self.to),
            'subject': self.subject,
            'html': self.html
        }
        
        if self.from_email:
            payload['from'] = str(self.from_email)
            if self.from_email.name:
                payload['name'] = self.from_email.name

        if self.reply_to:
            payload['reply_to'] = str(self.reply_to)

        if self.headers:
            payload['headers'] = self.headers

        if self.attachments:
            payload['attachments'] = [att.to_dict() for att in self.attachments]

        return payload