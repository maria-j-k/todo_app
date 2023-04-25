import base64
import os
from email.mime.text import MIMEText

from fastapi import HTTPException
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from pydantic import AnyUrl, EmailStr
from requests import HTTPError

from app.config import settings

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

MESSAGE = """
Click the link to reset your password:
{url}
The link is valid for {link_validity} minutes.
After this time you can request another password reset email.
If you didn't request the password change, please ignore this message.
Kind regards,
    ToDo app team
"""


async def send_message(email: EmailStr, url: AnyUrl):
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=33287)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    service = build("gmail", "v1", credentials=creds)
    message = MIMEText(
        MESSAGE.format(url=url, link_validity=settings.email_token_expires)
    )
    message["to"] = email
    message["subject"] = "Password recovery request"
    create_message = {"raw": base64.urlsafe_b64encode(message.as_bytes()).decode()}
    try:
        message = (
            service.users().messages().send(userId="me", body=create_message).execute()
        )
        print(f'Sent message to {message}. Message Id: {message["id"]}')
    except HTTPError as error:
        raise HTTPException(detail=error)