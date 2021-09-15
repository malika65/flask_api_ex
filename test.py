import requests

BASE = 'http://127.0.0.1:5000/'

data = [{"likes":10,"name":"How to make ball","views":1600},
        {"likes":1000,"name":"Write REST API","views":8000},
        {"likes":8000,"name":"Replace you ego","views":16000}
        ]

for i in range(len(data)):
    response = requests.put(BASE + 'helloworld/'+str(i), data[i])
    print(response.json())

input()
response = requests.delete(BASE + 'helloworld/0')
print(response)# as we return not json serializable obj we do not need put .json(), it will return error
input()
response = requests.get(BASE + 'helloworld/2')
print(response.json())