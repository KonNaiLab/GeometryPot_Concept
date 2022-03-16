import requests
import os
#os.environ['NO_PROXY'] = '127.0.0.1'
x = requests.get("http://127.0.0.1:5555/status/1/all")
print(x)