from datetime import date
import os
import sys
import smtplib
import random
from email.message import EmailMessage
from email.headerregistry import Address

from juniorguru.lib.log import get_log
from juniorguru.send import job_metrics, logo_metrics


log = get_log('send')


EMAIL_BATCHES = (
    (job_metrics, 'Monday?', lambda date: date.weekday() == 0),
    (logo_metrics, 'First day of the month?', lambda date: date.today().day == 1),
)


def main():
    config = os.environ
    debug = os.getenv('DEBUG', '--debug' in sys.argv)
    log.info(f"Debug: {'YES' if debug else 'NO'}")
    today = date.today()
    log.info(f"Today: {today:%Y-%m-%d}")

    for module, when_label, when in EMAIL_BATCHES:
        log.info(f"About to send {module.__name__}")
        if when(today):
            log.error(f"{when_label} YES")
        else:
            log.error(f"{when_label} NO")
            if debug:
                log.info('Debug mode suppressed early exit')
            else:
                continue

        messages = list(module.generate_messages(today))
        log.info(f"The {module.__name__} generated {len(messages)} messages")

        if config.get('SMTP_ENABLED'):
            log.debug('Sending enabled')

            if debug:
                sample_message = random.choice(messages)
                log.info(f"Debug mode chose a message '{sample_message['subject']}'")
                messages = [debug_message(sample_message)]

            server = smtplib.SMTP(host=config['SMTP_HOST'],
                                  port=int(config['SMTP_PORT']))
            server.starttls()
            server.login(config['SMTP_USERNAME'], config['SMTP_PASSWORD'])
            try:
                for message in messages:
                    log.debug(f"Sending message '{message['subject']}'")
                    server.send_message(envelope(message))
                    log.info(f"Sent message '{message['subject']}'")
            finally:
                server.quit()
        else:
            log.warning('Sending not enabled')


def debug_message(message):
    return {**message, **dict(
        to_emails=[(name, 'ahoj@junior.guru') for
                    name, email_address in message['to_emails']],
        subject=f"[DEBUG] {message['subject']}",
        bcc_emails=[]
    )}


def envelope(message):
    em = EmailMessage()

    display_name, addr_spec = message['from_email']
    em['From'] = Address(display_name=display_name, addr_spec=addr_spec)

    em['To'] = [Address(display_name=display_name, addr_spec=addr_spec)
                for display_name, addr_spec in message['to_emails']]

    if message.get('bcc_emails'):
        em['Bcc'] = [Address(display_name=display_name, addr_spec=addr_spec)
                     for display_name, addr_spec in message['bcc_emails']]

    em['Subject'] = message['subject']
    em.add_header('Content-Type', 'text/html; charset="utf-8"')
    em.set_payload(message['html_content'].encode('utf-8'))
    return em


if __name__ == '__main__':
    main()
