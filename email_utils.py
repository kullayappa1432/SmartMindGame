"""
📧 EMAIL UTILITIES FOR PASSWORD RESET
======================================
Handles sending OTP and password reset emails.
"""

from flask import render_template_string
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv

load_dotenv()

mail = Mail()


def send_otp_email(user_email, username, otp):
    """
    Send OTP to user's email
    
    Args:
        user_email (str): User's email address
        username (str): User's username
        otp (str): 6-digit OTP
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        subject = "🔐 SmartMind - Verify Your Email (OTP: {})".format(otp)
        
        html_body = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px; text-align: center; border-radius: 10px 10px 0 0;">
                <h1 style="color: white; margin: 0;">🔐 Password Reset</h1>
            </div>
            
            <div style="background: #f8f9fa; padding: 40px; border-radius: 0 0 10px 10px;">
                <p style="color: #333; font-size: 16px;">Hello <strong>{username}</strong>,</p>
                
                <p style="color: #666; font-size: 14px;">
                    We received a request to reset your password. 
                    Use the OTP below to verify your email address.
                </p>
                
                <div style="background: white; border: 2px solid #667eea; border-radius: 10px; padding: 25px; text-align: center; margin: 30px 0;">
                    <p style="color: #999; font-size: 12px; margin: 0 0 10px 0;">YOUR VERIFICATION CODE</p>
                    <h2 style="color: #667eea; font-size: 36px; letter-spacing: 5px; margin: 0; font-weight: bold;">{otp}</h2>
                    <p style="color: #999; font-size: 12px; margin: 10px 0 0 0;">Valid for 30 minutes</p>
                </div>
                
                <p style="color: #999; font-size: 12px; text-align: center; margin: 20px 0;">
                    ⏱️ <strong>This OTP expires in 30 minutes</strong>
                </p>
                
                <div style="background: #fff3cd; border-left: 4px solid #ffc107; padding: 12px; border-radius: 4px; margin: 20px 0;">
                    <p style="color: #856404; font-size: 13px; margin: 0;">
                        💡 <strong>Did you NOT request this?</strong> Ignore this email and your account will remain secure.
                    </p>
                </div>
                
                <p style="color: #999; font-size: 12px; margin-top: 30px; border-top: 1px solid #ddd; padding-top: 20px;">
                    Best regards,<br>
                    <strong>SmartMind Team</strong>
                </p>
            </div>
        </div>
        """
        
        msg = Message(
            subject=subject,
            recipients=[user_email],
            html=html_body
        )
        
        mail.send(msg)
        print(f"✅ OTP email sent to {user_email}")
        return True
        
    except Exception as e:
        print(f"❌ Error sending OTP email: {str(e)}")
        return False


def send_password_reset_confirmation(user_email, username):
    """
    Send password reset confirmation email
    
    Args:
        user_email (str): User's email address
        username (str): User's username
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        subject = "✅ Password Reset Successful"
        
        html_body = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px; text-align: center; border-radius: 10px 10px 0 0;">
                <h1 style="color: white; margin: 0;">✅ Password Updated</h1>
            </div>
            
            <div style="background: #f8f9fa; padding: 40px; border-radius: 0 0 10px 10px;">
                <p style="color: #333; font-size: 16px;">Hi <strong>{username}</strong>,</p>
                
                <p style="color: #666; font-size: 14px;">
                    Your password has been successfully reset. You can now log in with your new password.
                </p>
                
                <div style="background: #d4edda; border-left: 4px solid #28a745; padding: 12px; border-radius: 4px; margin: 20px 0;">
                    <p style="color: #155724; font-size: 13px; margin: 0;">
                        🔒 <strong>Your account is secure.</strong> If you didn't make this change, 
                        please contact support immediately.
                    </p>
                </div>
                
                <p style="color: #999; font-size: 12px; margin-top: 30px; border-top: 1px solid #ddd; padding-top: 20px;">
                    Best regards,<br>
                    <strong>SmartMind Security Team</strong>
                </p>
            </div>
        </div>
        """
        
        msg = Message(
            subject=subject,
            recipients=[user_email],
            html=html_body
        )
        
        mail.send(msg)
        print(f"✅ Confirmation email sent to {user_email}")
        return True
        
    except Exception as e:
        print(f"❌ Error sending confirmation email: {str(e)}")
        return False
