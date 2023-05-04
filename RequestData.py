
import requests
import json


class ReqestData:
    """
    Authentication
    get Element detail as per given API
    after creating Instance it will automatically write a Json file for Network Element.

    to get file for pyhsical link use function:
                                getphysicalLinkFrom_API()

    """
    
    def __init__(self, url_for_Auth="https://147.75.202.26/rest-gateway/rest/api/v1/auth/token", 
                 url_for_L2_API="https://147.75.202.26:8545/restconf/data/ietf-network:networks/network=L2Topology",
                 url_for_inventory= "https://147.75.202.26:8545/restconf/operations/nsp-inventory:find"
                # url_for_L2_API = "https://battlensp.nice.nokia.net:8544/sdn/api/v4/ietf/te/networks",
                 #url_for_config= "https://147.75.202.26:8546/wfm/api/v1/action-execution"
                 ):
        self.url_for_Auth = url_for_Auth
        self.url_for_L2_API = url_for_L2_API
        self.url_for_inventory= url_for_inventory
        #self.u
        #self.url_for_physical_link= url_for_physical_link
        self.token='0'
        self.authentication()
        self.getInventory()
        #self.getConfig()

    def authentication(self):
        #url = "https://battlensp.nice.nokia.net/rest-gateway/rest/api/v1/auth/token"

        payload = json.dumps({
          "grant_type": "client_credentials"
        })
        headers = {
          'Content-Type': 'application/json',
          'Authorization': 'Basic YWRtaW46Tm9raWFOc3AyQA=='
        }

        response = requests.request("POST", self.url_for_Auth, headers=headers, data=payload, verify=False)

        self.getDataFrom_API(response=response)
        print(response.text)



    print('#######################################################')
    #get elements detail from API
    def getDataFrom_API(self, response):
        token = json.loads(response.text)
        access_token = token["access_token"]

        #saving token for later use
        self.token= access_token
        print(token["access_token"])

        #take tocken out from here and then use iti in authorizatiioon
        #url = "https://battlensp.nice.nokia.net:8544/NetworkSupervision/rest/api/v1/networkElements?filter=neName%20LIKE%20'SRAN%25'"
        payload={}
        headers = {
          'Authorization': f'Bearer {access_token}'
        }

        response = requests.request("GET", self.url_for_L2_API, headers=headers, data=payload, verify=False)
        #converting string format into json
        json_data= json.loads(response.text)
        #make output preetier
        #pretty_json= json.dumps(json_data, indent=4)

        self.writeJson(json_data)

    def writeJson(self, jsonData):
        
        with open('L2Element.json', 'w') as file:
            json.dump(jsonData, file)
    
   

    """
    # Next Step
    def getConfig(self):
        print("you are in config")
        url = "https://147.75.202.26:8546/wfm/api/v1/action-execution" 
        payload = json.dumps({ "name": "nsp.https", 
                              "input": { "url": "https://147.75.202.27:8443/nfm-p/rest/api/v2/netw/NetworkElement/executeMultiCli/network%3A10.10.10.1", 
                                        "method": "PUT", 
                                        "cert": "/opt/nsp/os/ssl/certs/nsp/nsp.pem",
                                          "contentType": "application/json", 
                                          "body": [ "environment no more", "/admin display-config " ] } })
        headers = { 
            'Authorization':  f'Bearer {self.token}',
            'Content-Type': 'application/json', 
            'Cookie': 'NSPOSAPP1_JSESSIONID=B017A6633B8AF3E3A7EC38E70FEADED0; NSPOS_JSESSIONID=BFBA115E467460BEE1EA66A39287387A' } 
        response = requests.request("POST", url, headers=headers, data=payload, verify=False) 
        json_data= json.loads(response.text)
        print(json_data)
        self.writeconfigFile(json_data)

        
    
    def writeconfigFile(self, jsonData):
        with open('config.json', 'w') as file:
            json.dump(jsonData, file)

        pass
    """

    def getInventory(self):
         

        #url = "https://147.75.202.26:8545/restconf/operations/nsp-inventory:find"

        payload = json.dumps({
        "nsp-inventory:input": {
            "xpath-filter": "/nsp-equipment:network/network-element",
            "depth": 5,
            "sort-by": [
            "name",
            "ne-name"
            ]
        }
        })
        headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {self.token}'
        }

        response = requests.request("POST", self.url_for_inventory, headers=headers, data=payload,verify=False)
        json_data= json.loads(response.text)
        #make output preetier
        #pretty_json= json.dumps(json_data, indent=4)
        #print(response.text)
        with open('Inventory.json', 'w') as file:
            json.dump(json_data, file)


    # def getphysicalLinkFrom_API(self):
    #     payload={}
    #     headers = {
    #       'Authorization': f'Bearer {self.token}'
    #     }

    #     response = requests.request("GET", self.url_for_physical_link, headers=headers, data=payload, verify=False)
    #     #converting string format into json
    #     json_data= json.loads(response.text)
    #     #make output preetier
    #     #pretty_json= json.dumps(json_data, indent=4)
          
    #     if json_data!= "":
    #       with open('physical_Link.json', 'w') as file:
    #           json.dump(json_data, file)
          
    
        

    def getToken(self):
        #print(self.token)
        return self.token
        

   # Authentication()

if __name__== "__main__":
   auth= ReqestData()
   print(auth.getToken())
  
   #auth.getDataFrom_API()
