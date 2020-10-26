import requests
url = 'http://96.66.89.62/scripts/directory.php'
url = '8.8.8.8'
data = {'dir': '../', 'outfile':'directory.json','options':'JSON_PRETTY_PRINT'}
r = requests.post(url)
print(r.content)

