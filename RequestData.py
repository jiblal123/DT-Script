
import requests
import json


class ReqestData:
    """
    This class is  used  to retrieve details of an element from  provided APIs. 
    After creating an instance, two JSON files will be generated automatically for the network element.
     Although writing  JSON files is not necessary, it can be helpful to visualize the data structure and navigate through it. 
     the data extraction can be done without creating a file. Just storing in a varaible is enough  

    

    """
                                        # authentican API
    def __init__(self, url_for_Auth="https://{{server}}/rest-gateway/rest/api/v1/auth/token", 
                 # Network topology API
                 url_for_L2_API="https://{{server}}:8545/restconf/data/ietf-network:networks/network=L2Topology", 
                 # Network inventory API, From here we can retrieve network devices related data like Card detail, Chassis, Software Version etc-
                 url_for_inventory= "https://{{server}}:8545/restconf/operations/nsp-inventory:find" 
                # url_for_L2_API = "https://battlensp.nice.nokia.net:8544/sdn/api/v4/ietf/te/networks",
                #Token_Termination = https://{'server'}/rest-gateway/rest/api/v1/auth/revocation   # Post request need to be made to terminate token

                #       This is an API for retriving Configuration file, but currently it is not used. Getting Data from API is faster than SSH connection
                #       but it is not used currently,  It can be used easily whenever bit more speed in exectuation is needed
                #url_for_config= "https://{{server}}:8546/wfm/api/v1/action-execution" 
                 ):
        
        self.url_for_Auth = url_for_Auth
        self.url_for_L2_API = url_for_L2_API
        self.url_for_inventory= url_for_inventory
        
        self.token='0' #Storing Token so that later token managemnt stuff can be done
        # 
        self.authentication()
        self.getInventory()
        #self.getConfig()

    def authentication(self):
        """This function calls the authentication API using the provided credentials. 
        If the credentials are correct, the API returns an access token in string format, which is required to call the API pro-vided by NSP. 
        If the access token is not available, the API does not return the topology data.
        Therefore, the access token sent by the authentication API is stored in the token variable """
        #url = "https://battlensp.nice.nokia.net/rest-gateway/rest/api/v1/auth/token"

        payload = json.dumps({
          "grant_type": "client_credentials"
        })
        headers = {
          'Content-Type': 'application/json',
          'Authorization': 'Basic xxxxxxxxxx=='  # The postman is used to understand how Authenticantion API call works using the NSP Username and password and postman gives this type of header for Python request. 
        }

        response = requests.request("POST", self.url_for_Auth, headers=headers, data=payload, verify=False) # Veryf= false is used (not given by potman) to disable SSL/TLS certificatate verifaction. If this is not used The Python throw error. Because the Client machine deos not currently have certificate to to establish a secure connection.
                                                                                                   #Verfiy= False, this parameter is not recommanded
         #saving token for later use                                                                    
        self.token = (json.loads(response.text))["access_token"]
        # calling Network Topology API
        self.getDataFrom_API(response=response)
        
        #print(response.text)



    
    #get elements detail from API
    def getDataFrom_API(self, response):
        """This function calls L2 Topology API and stored all data in l2Element.Json
        storing Data in file is not standard way of programming but For the sake of good visualisation and better understanding and navigation the data
        is stored in JSON file. Storing Data in a variable is a good way to go with"""
        token = json.loads(response.text)
        access_token = token["access_token"]

        payload={}
        headers = {
          'Authorization': f'Bearer {access_token}' # The Idea is taken from Postman 
        }

        response = requests.request("GET", self.url_for_L2_API, headers=headers, data=payload, verify=False) # Verify= false needed so the data can be used with out Certification but this way of programming is not recommanded. 
        # data came in String format it should be  converted into json
        json_data= json.loads(response.text)
        #make output preetier
        #pretty_json= json.dumps(json_data, indent=4)

        #Store in JSON
        self.writeJson(json_data)

    def writeJson(self, jsonData):
        
        with open('L2Element.json', 'w') as file:
            json.dump(jsonData, file)
    
   

    """
    # this is the way of calling Config API and getting Config Data
    def getConfig(self):
        print("you are in config")
        url = "https://{{server}}:8546/wfm/api/v1/action-execution" 
        payload = json.dumps({ "name": "nsp.https", 
                              "input": { "url": "https://{{server}}:8443/nfm-p/rest/api/v2/netw/NetworkElement/executeMultiCli/network%3A10.10.10.1", 
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
        """A JSON file Inventory is created and there the Inventory data is stored. JSON file is not needed storing Data in varibale is enough """

        #url = "https://{{server}}:8545/restconf/operations/nsp-inventory:find"

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
        """in case other API needed to be invoke, This function will provide the Token to enable API call outside of RequestData class
         For Token Managment is may use. After fininshing the use of Token it should be released. 
           """
        #print(self.token)
        return self.token
        

   # Authentication()

if __name__== "__main__":
   auth= ReqestData()
   print(auth.getToken())
  
   #auth.getDataFrom_API()
