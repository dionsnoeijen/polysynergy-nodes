import smtplib
import base64
from email.mime.base import MIMEBase
from email import encoders
from email.message import EmailMessage as RawEmail

from polysynergy_node_runner.setup_context.dock_property import dock_text_area, dock_property
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings


@node(
    'Send Email',
    'email',
    icon='email.svg',
)
class SendEmail(Node):
    smtp_host: str = NodeVariableSettings(label="Host", dock=True, has_in=True)
    smtp_port: int = NodeVariableSettings(label="Port", dock=True, has_in=True, default=587)
    smtp_user: str = NodeVariableSettings(label="User", dock=True, has_in=True)
    smtp_password: str = NodeVariableSettings(
        label="SMTP Password",
        dock=dock_property(
            enabled=False,
            info="Connect a secret (node) to set this value."
        ),
        has_in=True,
    )
    smtp_use_tls: bool = NodeVariableSettings(label="Use TLS", dock=dock_property(switch=True), default=True)

    sender: str = NodeVariableSettings(
        label="From",
        dock=dock_property(info='Sender email address, something like: Example <no-reply@example.com>'),
        has_in=True,
        default="Example <no-reply@example.com>"
    )
    recipient: str = NodeVariableSettings(label="To", dock=True, has_in=True)
    cc: str = NodeVariableSettings(label="CC", dock=True, has_in=True, default="")
    bcc: str = NodeVariableSettings(label="BCC", dock=True, has_in=True, default="")
    subject: str = NodeVariableSettings(label="Subject", dock=True, has_in=True)
    body: str = NodeVariableSettings(label="Body", dock=dock_text_area(info='For a html body, connect a template node.'), has_in=True)
    is_html: bool = NodeVariableSettings(label="Is HTML?", dock=dock_property(switch=True), default=True)

    attachments: list[dict] | dict | None = NodeVariableSettings(
        label="Attachments",
        has_in=True,
        default=None,
        info="Dict or list of dicts with 'filename', 'content' (base64), and optional 'mimetype'"
    )

    true_path: bool = PathSettings(label="Success")
    false_path: bool | dict = PathSettings(label="Error")

    def execute(self):
        try:
            if not all([self.smtp_host, self.smtp_user, self.smtp_password]):
                raise ValueError("SMTP config missing.")

            msg = RawEmail()
            msg['Subject'] = self.subject
            msg['From'] = self.sender
            msg['To'] = self.recipient
            if self.cc:
                msg['Cc'] = self.cc
            if self.bcc:
                msg['Bcc'] = self.bcc

            recipients = [self.recipient]
            if self.cc:
                recipients += [email.strip() for email in self.cc.split(',')]
            if self.bcc:
                recipients += [email.strip() for email in self.bcc.split(',')]

            msg.set_content(self.body, subtype="html" if self.is_html else "plain")

            for att in self.attachments or []:
                filename = att.get("filename", "attachment")
                content_b64 = att.get("content")
                mimetype = att.get("mimetype", "application/octet-stream")
                if not content_b64:
                    raise ValueError(f"Attachment '{filename}' has no content.")
                data = base64.b64decode(content_b64)
                maintype, subtype = mimetype.split("/", 1)
                part = MIMEBase(maintype, subtype)
                part.set_payload(data)
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", f'attachment; filename="{filename}"')
                msg.attach(part)

            server = smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=10)
            if self.smtp_use_tls:
                server.starttls()
            server.login(self.smtp_user, self.smtp_password)
            server.send_message(msg, to_addrs=recipients)
            server.quit()

            self.true_path = True

        except Exception as e:
            self.false_path = {'error': str(e)}