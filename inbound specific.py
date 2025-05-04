import json
import urllib.parse
import requests
from dotenv import load_dotenv
import os

load_dotenv()
panel_username = os.getenv('PANEL_USERNAME')
panel_url = os.getenv('PANEL_URL')
panel_port = os.getenv('PORT')
panel_pass = os.getenv('PANEL_PASS')
type = os.getenv('TYPE')
inbound_tag = os.getenv('INBOUND_TAG')

users = []

panel_url = panel_url+ ":" + panel_port
#panel auth :
pass_Temp = urllib.parse.quote_plus(panel_pass)
api_url = f"{panel_url}/api/admin/token"
headers_dict = {"accept" : "application/json" , "Content-Type" : "application/x-www-form-urlencoded" }
post_data = f"grant_type=password&username={panel_username}&password={pass_Temp}&scope=&client_id=&client_secret="
post_resault = requests.post(api_url , data=post_data , headers=headers_dict )
auth_data = json.loads(post_resault.text)
Authorization_api = auth_data["access_token"]
pass_Temp = " "

# get data :
url = f"{panel_url}/api/users"
dict = {"accept" : "application/json" , "Authorization" : f"Bearer {Authorization_api}"}
resault = requests.get(url,headers=dict)
data = json.loads(resault.text)

#inbound specific Check :
total = data["total"]
for i in range (0,total) :
    users.append(data["users"][i]["username"])
    inbounds = data["users"][i]["inbounds"][type]
    if inbound_tag in inbounds :
        print (users[i])
    
