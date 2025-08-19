import requests

url = "http://127.0.0.1:8000/api/chat"
payload = {"question": "Show me the carbon emissions for 2020-2023."}

response = requests.post(url, json=payload)

print("Status Code:", response.status_code)
print("Response JSON:", response.json())

