import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
from dotenv import load_dotenv

# Load from login/server/.env
env_path = os.path.join(os.path.dirname(__file__), '..', '..', 'login', 'server', '.env')
load_dotenv(env_path)

class EmailNotifier:
    @staticmethod
    def send_login_notification(client_id: str, name: str, kite_id: str, mode: str, login_time: datetime, date: str):
        """Send email notification when user starts the bot"""
        try:
            recipient_email = os.getenv('NOTIFICATION_EMAIL')
            if not recipient_email:
                print("NOTIFICATION_EMAIL not found in .env file")
                return
            
            subject = f"🟢 Bot Started - {name}"
            body = f"""
<html>
<body style="font-family: Arial, sans-serif;">
    <h2 style="color: #28a745;">Bot Login Notification</h2>
    <table style="border-collapse: collapse; width: 100%;">
        <tr>
            <td style="padding: 8px; border: 1px solid #ddd;"><strong>Client ID:</strong></td>
            <td style="padding: 8px; border: 1px solid #ddd;">{client_id}</td>
        </tr>
        <tr>
            <td style="padding: 8px; border: 1px solid #ddd;"><strong>Name:</strong></td>
            <td style="padding: 8px; border: 1px solid #ddd;">{name}</td>
        </tr>
        <tr>
            <td style="padding: 8px; border: 1px solid #ddd;"><strong>Kite ID:</strong></td>
            <td style="padding: 8px; border: 1px solid #ddd;">{kite_id}</td>
        </tr>
        <tr>
            <td style="padding: 8px; border: 1px solid #ddd;"><strong>Mode:</strong></td>
            <td style="padding: 8px; border: 1px solid #ddd;">{mode}</td>
        </tr>
        <tr>
            <td style="padding: 8px; border: 1px solid #ddd;"><strong>Login Time:</strong></td>
            <td style="padding: 8px; border: 1px solid #ddd;">{login_time.strftime('%I:%M:%S %p')}</td>
        </tr>
        <tr>
            <td style="padding: 8px; border: 1px solid #ddd;"><strong>Date:</strong></td>
            <td style="padding: 8px; border: 1px solid #ddd;">{date}</td>
        </tr>
    </table>
</body>
</html>
"""
            EmailNotifier._send_email(recipient_email, subject, body)
            print(f"✅ Login notification sent to {recipient_email}")
        except Exception as e:
            print(f"❌ Failed to send login notification: {e}")
    
    @staticmethod
    def send_logout_notification(client_id: str, name: str, kite_id: str, mode: str, 
                                 login_time: datetime, logout_time: datetime, 
                                 total_trades: int, net_pnl: float):
        """Send email notification when user stops the bot"""
        try:
            recipient_email = os.getenv('NOTIFICATION_EMAIL')
            if not recipient_email:
                print("NOTIFICATION_EMAIL not found in .env file")
                return
            
            pnl_color = "#28a745" if net_pnl >= 0 else "#dc3545"
            subject = f"🔴 Bot Stopped - {name}"
            body = f"""
<html>
<body style="font-family: Arial, sans-serif;">
    <h2 style="color: #dc3545;">Bot Logout Notification</h2>
    <table style="border-collapse: collapse; width: 100%;">
        <tr>
            <td style="padding: 8px; border: 1px solid #ddd;"><strong>Client ID:</strong></td>
            <td style="padding: 8px; border: 1px solid #ddd;">{client_id}</td>
        </tr>
        <tr>
            <td style="padding: 8px; border: 1px solid #ddd;"><strong>Name:</strong></td>
            <td style="padding: 8px; border: 1px solid #ddd;">{name}</td>
        </tr>
        <tr>
            <td style="padding: 8px; border: 1px solid #ddd;"><strong>Kite ID:</strong></td>
            <td style="padding: 8px; border: 1px solid #ddd;">{kite_id}</td>
        </tr>
        <tr>
            <td style="padding: 8px; border: 1px solid #ddd;"><strong>Mode:</strong></td>
            <td style="padding: 8px; border: 1px solid #ddd;">{mode}</td>
        </tr>
        <tr>
            <td style="padding: 8px; border: 1px solid #ddd;"><strong>Date:</strong></td>
            <td style="padding: 8px; border: 1px solid #ddd;">{logout_time.strftime('%Y-%m-%d')}</td>
        </tr>
        <tr>
            <td style="padding: 8px; border: 1px solid #ddd;"><strong>Login Time:</strong></td>
            <td style="padding: 8px; border: 1px solid #ddd;">{login_time.strftime('%I:%M:%S %p')}</td>
        </tr>
        <tr>
            <td style="padding: 8px; border: 1px solid #ddd;"><strong>Logout Time:</strong></td>
            <td style="padding: 8px; border: 1px solid #ddd;">{logout_time.strftime('%I:%M:%S %p')}</td>
        </tr>
        <tr>
            <td style="padding: 8px; border: 1px solid #ddd;"><strong>Total Trades:</strong></td>
            <td style="padding: 8px; border: 1px solid #ddd;">{total_trades}</td>
        </tr>
        <tr>
            <td style="padding: 8px; border: 1px solid #ddd;"><strong>Net P&L:</strong></td>
            <td style="padding: 8px; border: 1px solid #ddd; color: {pnl_color}; font-weight: bold;">₹{net_pnl:.2f}</td>
        </tr>
    </table>
</body>
</html>
"""
            EmailNotifier._send_email(recipient_email, subject, body)
            print(f"✅ Logout notification sent to {recipient_email}")
        except Exception as e:
            print(f"❌ Failed to send logout notification: {e}")
    
    @staticmethod
    def _send_email(to_email: str, subject: str, html_body: str):
        """Internal method to send email using Gmail SMTP"""
        sender_email = os.getenv('SMTP_EMAIL')
        sender_password = os.getenv('SMTP_PASSWORD')
        smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.getenv('SMTP_PORT', '587'))
        
        if not sender_email or not sender_password:
            print("SMTP_EMAIL or SMTP_PASSWORD not found in login/server/.env file")
            return
        
        msg = MIMEMultipart('alternative')
        msg['From'] = sender_email
        msg['To'] = to_email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(html_body, 'html'))
        
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
