import json

data = {
	"images" : [
	]
}

with open('test_data.json','w') as outfile:
        json.dump(data,outfile)

