from Filter import DataExtractionFromJson
from RequestData import ReqestData
from cards import card
import yaml
import json


class CreateTopology():
    myTopology = {
        "name": "JibTopology",
        "topology":{
        
        "nodes":{ },
        "links":[],
         
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
    # give each node: name, kind, group, image, type, license
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
            nodeDetail['image']=  f"registry.srlinux.dev/pub/vr-sros:{versionandChassis[0]}" # with [0] device version  and with [1] chassis
            nodeDetail['type']= f"cp: cpu=2 ram=6 chassis={versionandChassis[1]} slot=A card={pc} ___ lc: cpu=2 ram=6 max_nics=10 chassis={versionandChassis[1]} slot=1 card={lc} mda/1={mda}"
            nodeDetail["startup-config"]= f"{nodename}config.txt"
            
            #nodeDetail["type2"] = "cp: cpu=2 ram=6 chassis=SR-2s slot=A card=cpm-2s ___ lc: cpu=2 ram=6 max_nics=10 chassis=SR-2s slot=1 card=xcm-2s mda/1=s18-100gb-qsfp28"
            nodeDetail['license']= "license.txt"

           
            self.Node_for_Yaml.append(nodeDetail)
        
    def updateTopology(self):
        
        for element in self.Node_for_Yaml:
            self.nodeTemplate= node()
        
            self.nodeTemplate.nodes[element["name"]]= self.nodeTemplate.nodes.pop("NeName")
            self.nodeTemplate.nodes[element["name"]]["kind"]= element['kind']
            self.nodeTemplate.nodes[element["name"]]["group"]= element['group']
            self.nodeTemplate.nodes[element["name"]]["image"]= element['image']
            self.nodeTemplate.nodes[element["name"]]["type"]= element['type']
            self.nodeTemplate.nodes[element["name"]]["license"]= element['license']
            self.nodeTemplate.nodes[element["name"]]["startup-config"]= element['startup-config']
            self.myTopology["topology"]['nodes'].update(self.nodeTemplate.nodes)

           
        

    def createYAMLFile(self):
        self.myTopology["name"]= self.topologyName
        with open('L2topology.yaml', 'w') as file:
            yaml.safe_dump(self.myTopology, file ,default_flow_style=False,sort_keys= False, indent=4 )
            
    def addLink(self):
        #endpind= str(["R2-PE:eth-1", "R4-P:eth-1"])
        for link in self.link.values():
           # print(link)

            self.myTopology["topology"]['links'].append({
                    "endpoints": link
                }) 
        