
# Create your views here.
import pyotp
from twilio.rest import Client
import re 

def otp_generate():
    secret = pyotp.random_base32()
    totp = pyotp.TOTP(secret)
    return totp.now()


def otp_request_twillo(mobile_no, msg):
    account_sid = 'AC7716acf04aa71375e3edf153d709bf06'
    auth_token = '1bb79a067e2b8ce7c11eb579706ffe00'
    client = Client(account_sid, auth_token)
    message = client.messages \
                    .create(
                        body=msg,
                        from_='+12546137646',
                        to=f"+91{mobile_no}"
                    )
    print('sent.................................')
    return

  
regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'  
def email_check_validation(email):   
    if(re.search(regex,email)):   
        return True
    else:   
        return False 
      