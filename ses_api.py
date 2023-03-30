import boto3

class SESAPI:
    def __init__(self, access_key: str, secret_key: str, region_name: str):
        self.ses_client = boto3.client('ses', aws_access_key_id=access_key, aws_secret_access_key=secret_key, region_name=region_name)

    def send_email(self, from_email: str, to_emails: list, subject: str, body: str, cc_emails: list = None, bcc_emails: list = None):
        message = {
            'Subject': {
                'Data': subject
            },
            'Body': {
                'Text': {
                    'Data': body
                }
            }
        }
        destination = {
            'ToAddresses': to_emails
        }
        if cc_emails:
            destination['CcAddresses'] = cc_emails
        if bcc_emails:
            destination['BccAddresses'] = bcc_emails
        response = self.ses_client.send_email(Source=from_email, Destination=destination, Message=message)
        return response['MessageId']

    def list_verified_email_addresses(self):
        response = self.ses_client.list_verified_email_addresses()
        return response['VerifiedEmailAddresses']

    def verify_email_address(self, email_address: str):
        response = self.ses_client.verify_email_address(EmailAddress=email_address)
        return response['VerificationToken']

    def delete_verified_email_address(self, email_address: str):
        self.ses_client.delete_verified_email_address(EmailAddress=email_address)
        
# Create an instance of the SESAPI class
ses_api = SESAPI(access_key='your_access_key', secret_key='your_secret_key', region_name='your_region_name')

# Send an email
from_email = 'sender@example.com'
to_emails = ['recipient1@example.com', 'recipient2@example.com']
cc_emails = ['cc1@example.com', 'cc2@example.com']
bcc_emails = ['bcc1@example.com', 'bcc2@example.com']
subject = 'Test email'
body = 'Hello, this is a test email!'
message_id = ses_api.send_email(from_email=from_email, to_emails=to_emails, subject=subject, body=body, cc_emails=cc_emails, bcc_emails=bcc_emails)
print(f'Sent email with message ID: {message_id}')

# List all verified email addresses
print(ses_api.list_verified_email_addresses())

# Verify a new email address
email_address = 'new_email@example.com'
verification_token = ses_api.verify_email_address(email_address=email_address)
print(f'Verification token for {email_address}: {verification_token}')

# Delete a verified email address
email_address = 'old_email@example.com'
ses_api.delete_verified_email_address(email_address=email_address)
print(f'Deleted verified email address: {email_address}')
