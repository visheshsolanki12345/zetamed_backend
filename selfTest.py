import pyotp
import time
totp = pyotp.TOTP('base32secret3232')
otp = totp.now() # => '492039'

# OTP verified for current time
print(totp.verify(otp)) # => True
time.sleep(30)
print(totp.verify(otp)) # => False