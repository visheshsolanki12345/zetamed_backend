import pyotp
from twilio.rest import Client
import re 

def otp_generate():
    secret = pyotp.random_base32()
    totp = pyotp.TOTP(secret)
    return totp.now()


def otp_request_twillo(mobile_no, msg):
    set_signal = ''
    try:
        account_sid = 'AC7716acf04aa71375e3edf153d709bf06'
        auth_token = 'c327fe01d72a1d53b5bc37e0a67090fa'
        client = Client(account_sid, auth_token)
        message = client.messages \
                        .create(
                            body=msg,
                            from_='+12546137646',
                            to=f"+91{mobile_no}"
                        )
        
        set_signal = True
        return set_signal, message.sid
    except:
        set_signal = False
        return set_signal, ''


  
regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'  
def email_check_validation(email):   
    if(re.search(regex,email)):   
        return True
    else:   
        return False 
      