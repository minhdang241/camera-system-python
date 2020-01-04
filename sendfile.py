import requests
files = {'video': open('video7.mp4', 'rb')}
response = requests.post('http://192.168.0.101:3000/upload', files=files)
print(response.text)
print('hello')
