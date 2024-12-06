"""
Example of Flask integration with Shoutbox
"""

from flask import Flask, request, jsonify
from shoutbox import ShoutboxClient, Email, EmailAddress, Attachment
import os

app = Flask(__name__)

# Initialize Shoutbox client
client = ShoutboxClient(api_key=os.getenv('SHOUTBOX_API_KEY'))

@app.route('/send-email', methods=['POST'])
def send_email():
    """Basic email sending endpoint"""
    try:
        data = request.json
        
        email = Email(
            from_email=data.get('from', 'sender@yourdomain.com'),
            to=data['to'],
            subject=data['subject'],
            html=data['html']
        )
        
        response = client.send(email)
        return jsonify({'success': True, 'response': response})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/send-email-with-attachment', methods=['POST'])
def send_email_with_attachment():
    """Email sending endpoint with file attachment support"""
    try:
        # Get file from request
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
            
        file = request.files['file']
        
        # Create attachment
        attachment = Attachment(
            filename=file.filename,
            content=file.read(),
            content_type=file.content_type
        )
        
        # Create email with attachment
        email = Email(
            from_email=request.form.get('from', 'sender@yourdomain.com'),
            to=request.form['to'],
            subject=request.form['subject'],
            html=request.form['html'],
            attachments=[attachment]
        )
        
        response = client.send(email)
        return jsonify({'success': True, 'response': response})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/send-bulk-email', methods=['POST'])
def send_bulk_email():
    """Endpoint for sending emails to multiple recipients"""
    try:
        data = request.json
        
        email = Email(
            from_email=data.get('from', 'sender@yourdomain.com'),
            to=data['to'],  # List of recipients
            subject=data['subject'],
            html=data['html'],
            headers=data.get('headers', {})
        )
        
        response = client.send(email)
        return jsonify({'success': True, 'response': response})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# Example of a form submission handler
@app.route('/contact-form', methods=['POST'])
def handle_contact_form():
    """Handle contact form submission"""
    try:
        data = request.form
        
        # Create email from form data
        email = Email(
            from_email=EmailAddress(
                data['email'],
                data.get('name', '')
            ),
            to='contact@yourdomain.com',
            subject=f"Contact Form: {data['subject']}",
            html=f"""
                <h2>Contact Form Submission</h2>
                <p><strong>From:</strong> {data.get('name', 'Not provided')} ({data['email']})</p>
                <p><strong>Subject:</strong> {data['subject']}</p>
                <p><strong>Message:</strong></p>
                <p>{data['message']}</p>
            """
        )
        
        response = client.send(email)
        return jsonify({'success': True, 'message': 'Thank you for your message!'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

if __name__ == '__main__':
    # For testing purposes
    app.run(debug=True)

"""
Example usage with curl:

# Basic email
curl -X POST http://localhost:5000/send-email \
    -H "Content-Type: application/json" \
    -d '{
        "to": "recipient@example.com",
        "subject": "Test Email",
        "html": "<h1>Hello!</h1><p>This is a test email.</p>"
    }'

# Email with attachment
curl -X POST http://localhost:5000/send-email-with-attachment \
    -F "to=recipient@example.com" \
    -F "subject=Test Email with Attachment" \
    -F "html=<h1>Hello!</h1><p>This email has an attachment.</p>" \
    -F "file=@/path/to/file.pdf"

# Bulk email
curl -X POST http://localhost:5000/send-bulk-email \
    -H "Content-Type: application/json" \
    -d '{
        "to": ["recipient1@example.com", "recipient2@example.com"],
        "subject": "Bulk Test Email",
        "html": "<h1>Hello!</h1><p>This is a bulk test email.</p>"
    }'

# Contact form
curl -X POST http://localhost:5000/contact-form \
    -F "name=John Doe" \
    -F "email=john@example.com" \
    -F "subject=Test Contact" \
    -F "message=This is a test contact form submission."
"""
