import json

class DataExtractionFromJson():

    def __init__(self, networkId ="") -> None:
        #print("Instance of DataExtractionFromJson created")
        
        
        self.networkId = networkId # getting network ID
        #self.List_of_nodeId =[]
        #self.List_of_LinkId =[]
        self.Nodes_in_List_Dict_format={} # to store Nodes detail
        self.links_in_List_dict_format=[] # to store Link details
        self.nodeName_ID={} # storing node name and id


        self.nodeName=[] # storing only nodeName
        self.links_with_ports={} # storing link with ports
        self.data = "" # storing row data from JSON file
        self.loadData() #1. to run
        
        self.getNodes() #2. to run
        self.getNodesName()
        
        
        self.getLinks()  #3. to run
        

    def loadData(self):
        """this Function to load data from Json.
          Again, this is not a required step. The data could be stored in a variable, 
          and that variable can be used here to filter the data. However, this is done to see 
          the data structure and have good visibility of the data in the Json file because 
          printing data does not have good visual appeal."""
                
        # Open the JSON file
        with open('L2Element.json') as f:
            # Load the contents of the file into a Python object
            self.data = json.load(f)
        #print((self.data['ietf-network:network'][0]))
        self.networkId= self.data['ietf-network:network'][0]['network-id']
        #print("###################", self.networkId)

        #print((self.networkId))
        
        

    def getNodes(self):
        """Navigation to get the location where the actual data is located."""
        #print(self.networkId)
        self.Nodes_in_List_Dict_format = self.data['ietf-network:network'][0]['node']
        #print("Length of node", len(self.Nodes_in_List_Dict_format))
        #GetNode ID

        #self.List_of_nodeId =  list(self.Nodes_in_List_Dict_format.keys())
        #print(type(self.Nodes_in_List_Dict_format))
        #print(self.List_of_nodeId)

    def getNodesName(self):
        """get node name and node id as example follows: [{'10.10.10.8': 'R8-PE'},{'10.10.10.7': 'R7-PE-ASBR'}]"""
        for node in self.Nodes_in_List_Dict_format:
            name= node["ietf-l2-topology:l2-node-attributes"]["name"]
            id  = node["node-id"]
            Name_ID= {}
            Name_ID[id]= name

            #print((Name_ID))
            self.nodeName.append(Name_ID) #nameid: name
            self.nodeName_ID.update(Name_ID)

            
            #print("###########",node["ietf-l2-topology:l2-node-attributes"]["name"])
        #print(len(self.nodeName))
        #print("node id dict key" , list(self.nodeName_ID.keys()))


            
   
    def getLinks(self):
        """getting Link from the API data. The link from the API data may have a port name that needs to be renamed to fit the YAML syntax for containerlab topology.
        
        for example: port name of R2-P node is 1/1/1 but in YAML file the named must be eth1 for vrSros kind of node. For SRL its eth-1

        How the link is formated, is deeply defined in the Bachelor thesis for which this program is created.
        """

        # "ietf-l2-topology:l2-link-attributes"
        self.links_in_List_dict_format = self.data['ietf-network:network'][0]["ietf-network-topology:link"]
        #print(self.links_in_List_dict_format)
        a=0
        for link in self.links_in_List_dict_format:
           # print("Total link", len(self.links_in_List_dict_format))
            individualLink=[]
            
            individualLink = link["link-id"].split("--")

            # check if Id contain in self.nodeName
            # then send for rename
            firstNode= individualLink[0].split(":")[0]
            secondNode = individualLink[1].split(":")[0]
            #print(firstNode, secondNode)
            #result= self.checkifKeyContain(firstNode, secondNode)
            if firstNode in self.nodeName_ID.keys() and secondNode in self.nodeName_ID.keys():
                #calling renamePort function for rename the port
                self.renamePort(individualLink)
            else:
                continue
            
            #print(individualLink)

            renamed= self.renamePort(individualLink)
            #print(individualLink)
            #break
            self.links_with_ports["link"+str(a+1)]= renamed
            a=a+1
        # print("self.links_with_ports", len(self.links_with_ports))
        #print((self.links_with_ports))
           
    # def checkifKeyContain(self,firstNode, secondNode ): 
    #     ## this algorithm finds if first node and second node are contain in link both must be contain
    #     FirstNodeSearch = [my_dict for my_dict in self.nodeName if firstNode in my_dict.keys()]
    #     secondNodeSearch = [my_dict for my_dict in self.nodeName if secondNode in my_dict.keys()]
    #     if not FirstNodeSearch or not secondNodeSearch: 
    #         # if first node or second node is not in link then return false
    #         #print(False,"first", firstNode,"second", secondNode)
    #         return False
        
    #     else:
    #         return True

    #     # Print the matching dictionaries
    #    # for my_dict in matching_dicts:
    #     #    print(f"Found key {key_to_search} in dictionary {my_dict}")

                





       # print(self.links_with_ports)


    def renamePort(self, individualLinks ):
        """this is a algorith to remane ports. For example port 1/1/2 into eth2
         this might only work for limited number of  vrSROS node. For other node the port name might be diffrent. 
        The best way to do it is creating a mapping function or table from with the portname can be translated easily with out using complex algorithm """
        link=[]
        for i in range(len(individualLinks)):
            Node= individualLinks[i].split(":")
            port= Node[1].replace("Port","").strip()
           
            port= port.split("/")
            


            #print((port))
            #print(port[len(port)-2])
            # port Rename 
            if len(port)==3 and  port[0]=="1" and port[1] == "1":
                Node[1]= "eth"+ port[2]  
            elif len(port)==3 and  port[0]=="1" and port[1] != "1":
                Node[1]= "eth"+ port[1] + port[2]
            elif len(port)==4 and  (port[len(port)-2]!="1") and port[len(port)-1]== "1":
                Node[1]= ("eth"+ port[2]).replace("c","") 
            else:
                print(individualLinks)
                
                #Node[1]= "eth"+"2" #("eth"+ port[2]).replace("c","") 
                raise(f"ports went wrong. go and look at remaneport() function see this Link: {individualLinks}" )

            # node rename:
            #find a node name with id
            Node[0]= self.nodeName_ID[Node[0]]
            


            Node= ":".join([Node[0], Node[1]])
            link.append(Node)

            # if (port[len(port)-2]) == "1" or (port[len(port)-2]) =="c1":
            #     Node[1]= "eth-"+ port[len(port)-1]
            # elif (port[len(port)-2]) != "1" or (port[len(port)-2]) !="c1":
            #     print("somethin")    
        return(link)
            
            

        #print(self.List_of_LinkId)
    
      
"""
"""



if __name__ =="__main__":

    obj1 = DataExtractionFromJson()
   # obj1.getLinks()

