import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random

def create_message(sender_email, receiver_email, subject, body):
    """Create the email message."""
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    return message

def send_email(receiver_email, otp ,sender_email = "eduflex012@gmail.com", password =  "zihn dwia nsio dufn"):
    """Send the OTP email using SMTP."""
    
    subject = "Your One-Time Password (OTP)"
    body = f"Hello,\n\nYour OTP for verification is: {otp}\n\nPlease use this OTP to complete your verification. The OTP will expire in a few minutes.\n\nThank you!"

    message = create_message(sender_email, receiver_email, subject, body)
    
    
    server = smtplib.SMTP("smtp.gmail.com", 587)  
    server.starttls()  
    
    
    server.login(sender_email, password)
    
    
    server.sendmail(sender_email, receiver_email, message.as_string())
    
    
    server.quit()
    
    print("OTP email sent successfully!")

def generate_otp():
    """Generate a 6-digit OTP."""
    otp = random.randint(100000, 999999)
    return otp



if __name__ == '__main__':

    
    sender_email = "eduflex012@gmail.com"
    receiver_email = "dheerajgupta5432@gmail.com"
    password = "zihn dwia nsio dufn"

    
    otp = generate_otp()

    
    send_email(sender_email, receiver_email, otp, password)
