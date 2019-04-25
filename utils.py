import requests
import json
from datetime import datetime
import simplejson
base_url = "https://api.groupme.com/v3"
token = "Tcksyw8JOjESRGyYffr0o3IL2qcyNZ6EXBiy9Cc5"

headers = {
    'Content-Type': 'application/json;charset=UTF-8',
    'X-Access-Token': token
}

class Util:

    def __init__(self, temp_token):
        self.token = token

    def ask_for(self, url, params=None):
        return requests.get(base_url+url, params=params,headers=headers).json()['response']

    def get_msgs(self, group_id):
        params ={'limit': 100}
        response = requests.get(base_url + '/groups/'+group_id+'/messages',
                                headers = headers, params=params).json()
        
        code = response['meta']['code']
        
        if code != 304:
            messages = response['response']['messages']

        if not messages:
            raise StopIteration
        
        params['before_id'] = messages[-1]['id']


        while code != 304:
            for message in messages:
                yield {'name': message['name'],
                       'text': message['text'],
                       'date': datetime.fromtimestamp(message['created_at']),
                       'images': [x["url"] for x in message['attachments'] if x["type"]=="image"],
                       'liked': message['favorited_by']
                       }
            try:
                messages = requests.get(base_url + '/groups/'+group_id+'/messages',
                                        headers = headers, params=params).json()['response']['messages']
            except:
                raise StopIteration
            if messages:
                params['before_id'] = messages[-1]['id']
