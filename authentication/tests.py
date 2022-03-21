from twilio.rest import Client

account_sid = 'AC7716acf04aa71375e3edf153d709bf06'
auth_token = '1bb79a067e2b8ce7c11eb579706ffe00'


client = Client(account_sid, auth_token)
message = client.messages \
                .create(
                    body="hello",
                    from_='+12546137646',
                    to=f"+91{8878401574}"
                )

# import http.client

# conn = http.client.HTTPSConnection("api.msg91.com")

# payload = "{\n  \"flow_id\": \"623487dde51fb83c2b4b0da2\",\n  \"sender\": \"Zetamd\",\n  \"mobiles\": \"918878401574\",\n  \"COMPANY_NAME\": \"12345  1\",\n  \"OTP\": \"13254356 \"\n}"

# headers = {
#     'authkey': "374023AsJ3nBuTOn622430fbP1",
#     'content-type': "application/JSON"
#     }

# conn.request("POST", "/api/v5/flow/", payload, headers)

# res = conn.getresponse()
# data = res.read()

# print(data.decode("utf-8"))

