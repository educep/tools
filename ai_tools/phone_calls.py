"""
Created by Analitika at 09/12/2024
contact@analitika.fr
"""

# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client

# Set environment variables for your credentials
# Read more at http://twil.io/secure

account_sid = ""
auth_token = ""
client = Client(account_sid, auth_token)

call = client.calls.create(
    url="http://demo.twilio.com/docs/voice.xml",
    to="+330650900149",
    from_="+17753059692",
)

print(call.sid)
