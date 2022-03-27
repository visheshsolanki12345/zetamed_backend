# from django.test import TestCase

# Create your tests here.

# streaming = ['netflix', 'hulu', 'disney+', 'appletv+']

# index = streaming.index('disney+')
# print('The index of disney+ is:', streaming[index])


# from datetime import datetime

# import requests
# import json
# from fake_useragent import UserAgent


# keyword = "parac"
# keyword.replace(" ", "+")
# url = "http://suggestqueries.google.com/complete/search?output=firefox&q=" + keyword
# ua = UserAgent()
# headers = {"user-agent": ua.chrome}
# response = requests.get(url, headers=headers, verify=False)
# suggestions = json.loads(response.text)
# for word in suggestions[1]:
#   print(word)