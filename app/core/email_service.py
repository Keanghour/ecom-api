import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_reset_email(email: str, reset_token: str):
    # Send email logic here (using SMTP or an email API like SendGrid)
    msg = MIMEMultipart()
    msg["From"] = "noreply@example.com"
    msg["To"] = email
    msg["Subject"] = "Password Reset Request"
    
    body = f"Click the link to reset your password: http://example.com/reset-password?token={reset_token}"
    msg.attach(MIMEText(body, "plain"))
    
    # SMTP connection (use your own SMTP server)
    server = smtplib.SMTP("smtp.example.com", 587)
    server.starttls()
    server.login("your-email@example.com", "your-password")
    text = msg.as_string()
    server.sendmail("noreply@example.com", email, text)
    server.quit()
