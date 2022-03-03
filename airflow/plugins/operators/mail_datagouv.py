import logging
from typing import Optional

import emails
from airflow.models import BaseOperator


class MailDatagouvOperator(BaseOperator):
    """
    Send a mail
    :param email_user: sender of email
    :type email_user: str
    :param email_password: sender of email
    :type email_password: str
    :param email_recipients: recipients of email
    :type email_recipients: list
    :param subject: subject of email
    :type subject: str
    :param message: corpus of email
    :type message: str
    :param attachment_path: path of attachment for email
    :type attachment_path: str

    """

    supports_lineage = True

    template_fields = (
        "email_user",
        "email_password",
        "email_recipients",
        "subject",
        "message",
        "attachment_path",
    )

    def __init__(
        self,
        *,
        email_user: Optional[str] = None,
        email_password: Optional[str] = None,
        email_recipients: Optional[list] = None,
        subject: Optional[str] = None,
        message: Optional[str] = None,
        attachment_path: Optional[str] = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)

        self.email_user = email_user
        self.email_password = email_password
        self.email_recipients = email_recipients
        self.subject = subject
        self.message = message
        self.attachment_path = attachment_path

    def execute(self, context):
        if not self.email_user or not self.email_password:
            raise ValueError("Not enough information to send message")

        sender = self.email_user
        message = self.message
        subject = self.subject
        message = emails.html(
            html="<p>%s</p>" % message, subject=subject, mail_from=sender
        )

        smtp = {
            "host": "mail.data.gouv.fr",
            "port": 587,
            "tls": True,
            "user": self.email_user,
            "password": self.email_password,
            "timeout": 60,
        }
        if self.attachment_path:
            message.attach(
                data=open(self.attachment_path),
                filename=self.attachment_path.split("/")[-1],
            )

        retry = True
        tries = 0
        while retry:
            r = message.send(to=self.email_recipients, smtp=smtp)
            logging.info(r)
            tries = tries + 1
            if (r.status_code == 250) | (tries == 5):
                retry = False
        assert r.status_code == 250
