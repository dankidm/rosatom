import  requests

# Define the URL and data
url = "http://127.0.0.1:5000"
data = {
}

# Send the POST request
response = requests.post(url, json=data)

# Print the response
print("Status Code:", response.status_code)
print("Response Body:", response.json())

from time import sleep
sleep(5)

idd = "149add4a9efb4c28d95abfa35af3b95e7ec3e30cc7d4d33ebfee3313214113ca"
response = requests.get(url+f"/{idd}/segments")
# Print the response
print("Status Code:", response.status_code)
print("Response Body:", response.json())