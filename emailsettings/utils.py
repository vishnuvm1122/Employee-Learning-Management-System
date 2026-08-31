# mail_notifications/utils.py

from django.core.mail import EmailMessage, get_connection
from django.contrib import messages
from emailsettings.models import EmailSettings


def send_mail_notification(
    to_emails,
    subject: str,
    body: str,
    html_message: str = None,
    request=None
) -> bool:
    """
    Send email using configured EmailSettings.

    Args:
        to_emails (list): List of recipient emails
        subject (str): Email subject
        body (str): Plain text body
        html_message (str, optional): HTML content
        request (optional): Django request for messages framework

    Returns:
        bool: True if sent successfully, False otherwise
    """

    # ✅ Validate recipients
    if not to_emails:
        if request:
            messages.warning(request, "No recipient emails provided.")
        return False

    # ✅ Get active email settings
    email_settings = EmailSettings.objects.filter(email_enabled=True).first()
    if not email_settings:
        if request:
            messages.warning(request, "Email sending is disabled or not configured.")
        return False

    # ✅ Prepare connection config
    connection_params = {
        "host": email_settings.host,
        "port": email_settings.port,
        "use_tls": email_settings.use_tls,
        "use_ssl": email_settings.use_ssl,
    }

    if email_settings.username and email_settings.password:
        connection_params.update({
            "username": email_settings.username,
            "password": email_settings.password,
        })

    # ✅ Create connection
    try:
        connection = get_connection(**connection_params)
    except Exception as e:
        if request:
            messages.error(request, f"Email connection error: {str(e)}")
        return False

    # ✅ Prepare email
    from_email = email_settings.username or None

    try:
        email = EmailMessage(
            subject=subject,
            body=body,
            from_email=from_email,
            to=to_emails,
            connection=connection,
        )

        # ✅ HTML support
        if html_message:
            email.content_subtype = "html"
            email.body = html_message

        # ✅ Send email
        sent_count = email.send(fail_silently=False)

        if request:
            if sent_count:
                messages.success(request, f"Email sent successfully to {len(to_emails)} user(s).")
            else:
                messages.warning(request, "Email was not sent.")

        return sent_count > 0

    except Exception as e:
        if request:
            messages.error(request, f"Error sending email: {str(e)}")
        return False