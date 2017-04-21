import requests 
import json

url = "http://mea.labeeb-iot.com/uam_m2m/rest/UamCommunicationInterface"

# authenticate the user 
def auth_user():
	auth_data = {
	 	"enterpriseName": "IndoorAq",
	 	"userName": "cmu",
	 	"password": "omar$123"
	}

	r = requests.post(url+"/authenticate", json=auth_data)
	return {"JSESSIONID": r.cookies['JSESSIONID']}


# get the data 
def get_data(time=None):
	# authenticate first 
	session_id = auth_user()
	data = {}
	if time != None:
		new_time = str(time).replace(" ", "T")
		data = {'fromDate': new_time}

	response = requests.post(url+"/getData", json=data, cookies=session_id)
	return json.loads(response.text)
