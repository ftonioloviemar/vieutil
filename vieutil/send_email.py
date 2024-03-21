import smtplib
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders

user = 'sistema@viemar.com.br'

def send_email(
    to,
    subject,
    text,
    send_from=user,
    files=[],
    attachments=[],
    server='viemar-com-br.mail.protection.outlook.com',
    port=25,
    username=user,
    #password=pwd,
    use_tls=True
):
    """
    Compose and send email with provided info and attachments.
    Args:
        send_from (str): from name
        to (list[str]): to name(s)
        subject (str): message title
        text (str): message body
        files (list[str]): list of file paths to be attached to email
        attachments (list[[str, bytes]): list of lists with filename and binary content to be attached to email
        server (str): mail server host name
        port (int): port number
        username (str): server auth username
        password (str): server auth password
        use_tls (bool): use TLS mode
    """
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    for path in files:
        part = MIMEBase('application', "octet-stream")
        with open(path, 'rb') as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            'attachment; filename={}'.format(Path(path).name)
        )
        msg.attach(part)

    for att in attachments:
        part = MIMEBase('application', "octet-stream")
        filename, content = att
        part.set_payload(content)
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename={filename}'
        )
        msg.attach(part)

    smtp = smtplib.SMTP(server, port)
    if use_tls:
        smtp.starttls()
    #smtp.login(username, password)
    smtp.sendmail(send_from, to, msg.as_string())
    smtp.quit()
    return True