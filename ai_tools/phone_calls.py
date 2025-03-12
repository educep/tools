"""
Created by Analitika at 09/12/2024
contact@analitika.fr
"""

# Download the helper library from https://www.twilio.com/docs/python/install


from twilio.rest import Client

# Set environment variables for your credentials
# Read more at http://twil.io/secure

account_sid = ""
auth_token = ""
client = Client(account_sid, auth_token)

call = client.calls.create(
    url="http://demo.twilio.com/docs/voice.xml",
    to="+3306XXXXXX",
    from_="+1XXXXXXXXX",
)

print(call.sid)
