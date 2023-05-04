from Filter import DataExtractionFromJson
from RequestData import ReqestData
from cards import card
import yaml
import json



class node:
    def __init__(self) -> None:
        self.nodes= {
                "NeName":{
                    "kind": "",
                    "image":""
                }
        }

class CreateTopology():
    myTopology = {
        "name": "JibTopology",
        "topology":{
        
        "nodes":{
            
                },
        "links":[
            
        
            ],
            
        
        }
    }

    def __init__(self) -> None:
        dataExtraction = DataExtractionFromJson()
        requestdata= ReqestData()
        self.topologyName= dataExtraction.networkId
        self.nodeId = dataExtraction.nodeName
        print(list(self.nodeId[0].keys())[0])
        self.link = dataExtraction.links_with_ports
        self.nodeTemplate= {}
        self.Node_for_Yaml= []
        
        self.createNode_Detail_for_topology()
        
        self.updateTopology()
        
        self.addLink()
        self.createYAMLFile()
        print("successful")
        print("Config file / if a file is empty that node is not send data via SSH")
        #print(self.nodeId)
        #print(self.link)
        #self.getVersion()

    # give each node name, kind, group, image, type, license
    def createNode_Detail_for_topology(self):
        cardObject = card()
        
        for node in self.nodeId:
            nodeDetail={}
            nodename = list(node.values())[0] # way of extracting value from dicht
            #print((nodename))
            node_id  = list(node.keys())[0]
            print(node_id)
            versionandChassis= self.getVersion(node_id) # software version
            card_detail = cardObject.getcard(node_id, nodename)
            lc= card_detail["lc"]
            pc = card_detail["pc"]
            mda = card_detail['mda']
            nodeDetail["name"]= nodename
            nodeDetail["kind"]= 'vr-sros'
            nodeDetail['group']= "sros"
            nodeDetail['image']=  f"registry.srlinux.dev/pub/vr-sros:{versionandChassis[0]}" # with [0] version  and with [1] chassis
            nodeDetail['type']= f"cp: cpu=2 ram=6 chassis={versionandChassis[1]} slot=A card={pc} ___ lc: cpu=2 ram=6 max_nics=10 chassis={versionandChassis[1]} slot=1 card={lc} mda/1={mda}"
            
            #nodeDetail["type2"] = "cp: cpu=2 ram=6 chassis=SR-2s slot=A card=cpm-2s ___ lc: cpu=2 ram=6 max_nics=10 chassis=SR-2s slot=1 card=xcm-2s mda/1=s18-100gb-qsfp28"
            nodeDetail['license']= "license.txt"

           
            self.Node_for_Yaml.append(nodeDetail)
        #print(self.Node_for_Yaml)

        

    def updateTopology(self):
        
        for element in self.Node_for_Yaml:
            #print(element)
           

            self.nodeTemplate= node()
            
            self.nodeTemplate.nodes[element["name"]]= self.nodeTemplate.nodes.pop("NeName")
            self.nodeTemplate.nodes[element["name"]]["kind"]= element['kind']
            self.nodeTemplate.nodes[element["name"]]["group"]= element['group']
            self.nodeTemplate.nodes[element["name"]]["image"]= element['image']
            self.nodeTemplate.nodes[element["name"]]["type"]= element['type']
            
            self.nodeTemplate.nodes[element["name"]]["license"]= element['license']


           # print(self.nodeTemplate.nodes)
            self.myTopology["topology"]['nodes'].update(self.nodeTemplate.nodes)

           # print(element["name"], element["kind"])
        
        

    def createYAMLFile(self):
        self.myTopology["name"]= self.topologyName

        #print(self.myTopology)
        # yamlData = yaml.dump(self.myTopology, default_flow_style=False)
        # print(yamlData)
        with open('L2topology.yaml', 'w') as file:
            yaml.safe_dump(self.myTopology, file ,default_flow_style=False,sort_keys= False, indent=4 )
        # with open('topology2.yaml', 'w') as file:
        #             yaml.safe_dump(self.myTopology, file,default_flow_style=True,sort_keys= False, indent=2 )

     

    def addLink(self):
        #endpind= str(["R2-PE:eth-1", "R4-P:eth-1"])
        for link in self.link.values():
           # print(link)

            self.myTopology["topology"]['links'].append({
                    "endpoints": link
                }) 
        #print(self.myTopology)    
        

        #self.myTopology["topology"]['links'].append({'endpoints': ['R2-PE:eth-1', 'R4-P:eth-1']})

    def getVersion(self, node_id):
        version= "22.7.R1"
        with open("Inventory.json",'r') as file:
            data = json.load(file)
            
        data= data["nsp-inventory:output"]["data"]#[0]["version"]
        for a_node in data:
            if a_node["ne-id"] == node_id:
                version= str(a_node["version"]).replace("TiMOS-C-","")

                ChassisWithProduct = str(a_node["type"])
                justVersionOfChasis = self.getCleanedChassis(ChassisWithProduct)
                return [version, justVersionOfChasis ]
            else: continue
        
        return version
        
    def getCleanedChassis(self, Chassis):

        if " " in  Chassis:
            onlyChasisType= Chassis.split(" ")
            return onlyChasisType[1]
        elif "-" in Chassis:
            index = Chassis.index("-")
            onlyChasisType= Chassis[index+1:]
            return onlyChasisType

        #print(data)
    
        



    





if __name__ =="__main__":
    obj= CreateTopology()
    #print(obj.Node_for_Yaml)
    