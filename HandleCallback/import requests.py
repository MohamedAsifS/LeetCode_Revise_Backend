import requests 
header={
    ""
}
endpoint=requests.post("https://leetcode.com/api/submissions/")
print(endpoint.json())