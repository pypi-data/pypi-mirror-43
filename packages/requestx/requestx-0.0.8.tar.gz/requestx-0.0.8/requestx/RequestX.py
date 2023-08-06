import requests
class RequestX (object):

    def __init__(self):
        self.headers_json = {'Content-type': 'application/json', 'Accept': 'application/json'}
        self.headers_uri_list = {'Content-type': 'text/uri-list', 'Accept': 'application/json'}

    def post(self,data, url):
        return requests.post(url,json=data,headers=self.headers_json)
    
    def patch(self,data, url):
        return requests.patch(url,json=data,headers=self.headers_json)

    def get(self,url):
        return requests.get(url,headers=self.headers_json)
        
    def put_uri_list (self,data, url):
        return requests.put(url, data=data,headers=self.headers_uri_list)
    
