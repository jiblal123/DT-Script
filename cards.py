import paramiko 
import time 
import re
from Nodeconfig import config
class card():
    def __init__(self, ne_id= "10.10.10.5") -> None:
        self.config= config()
        
        # self.ne_id= ne_id
        # result= self.getcard(self.ne_id)
        # print(result)
        # self.cardDetail={}
        pass
    def getcard(self, ne_id, ne_name):
        # id to identify router , so that the configuration file can be rename as ne_name
        indexOfLastZiffer = ne_id.rfind(".")
        nodeName= ne_name
        #print("ne nameeeeeeeeeeeeeeeeeee",nodeName)
        
        print("index", indexOfLastZiffer)
        var= int(ne_id[indexOfLastZiffer+1:])
        print("last Ziffer", var)
        # creating SSH Tunnel and connectiong to the node with PuTTy Credentials
        client = paramiko.SSHClient() 
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
        client.connect('147.75.202.26', username='root', password='Changeme1!') 
        shell = client.invoke_shell() 
        time.sleep(2) 
        shell.send(f'ssh asad@192.168.100.{30+var}\r\n') # CLASSIC CLI 
        time.sleep(2) 
        shell.send('NokiaNsp!\r\n') # MD CLI 
        time.sleep(2) 
        shell.send('show card\r\n')
        time.sleep(2) 
        shell.send('show mda\r\n')
        time.sleep(2) # sleep stops program execution to allows tunnel  collect data.  
        # time.sleep(2) 
        # shell.send('show card state\r\n') 
        # time.sleep(2) 
        #output = shell.recv(1024).decode()
        outputCollection=""
        while shell.recv_ready(): 
            tmp = shell.recv(1024) 
        #     # if not tmp: 
        #     #     break 
            #print(tmp.decode())

            outputCollection= outputCollection + tmp.decode() +"\n" # collecting all output from Node. 
            # write the output to a text file
        with open('output.txt', 'w') as f:
            f.write(outputCollection)
            
        with open('output.txt', 'r') as f:
            data = f.read()
        result = self.get_pc_cP_mda(data)

        # for config in the same shh session
        self.config.getConfigFile(shell, nodeName)

        return result



    def get_pc_cP_mda(self, data):
        newlines= data.split("\n")
        newlines= [x for x in newlines if x]
        card1 = ""
        mda    = ""
        pc   =""
        #print(len(newlines))
        
        #print(newlines)
        #sentences = ['The quick brown fox', 'jumps over', 'the lazy dog']
        word = 'show card'
        #finding show card
        for line in newlines:
            if word in line:
                index= newlines.index(line)
                #print(f"{word} found in, index {index}")
                
                cardwithSlot= ' '.join(newlines[index+7].split()) # removing unnecessary white space
                card1= (cardwithSlot.split(" "))[1]
                #print(cardwithSlot.split(" "))
                #print(card1)
                #print(newlines[index+8])
                processorCard= ' '.join(newlines[index+8].split()) # removing unnecessary white space
                pc=             (processorCard.split(" "))[1]
                #print(processorCard)
                #print(pc)
            # else:
            #     raise(f"{word} not found in ")
        # finding mda  
        word ='MDA Summary'  
        for line in newlines:
            if word in line:
                index= newlines.index(line)
                #print(f"{word} found mda in, index {index}")
                
                mdaCardWithSlot= ' '.join(newlines[index+5].split()) # removing unnecessary white space
                mda            = (mdaCardWithSlot.split(" "))[2]
                #print(mdaCardWithSlot)
                #print(mda)
                # print(newlines[index+2])
                # processorCard= ' '.join(newlines[index+3].split())
                # print(processorCard)
            # else:
            #     raise(f"{word} not found in ")
        return {"lc":card1, "pc": pc, "mda":mda  }
    



if __name__ == "__main__":
    obj = card()
    result= obj.getcard("10.10.10.5")
    print("card:", result["card1"], "pc", result["pc"], "mda", result["mda"])    



       




    

    # pattern = r'(\d+)\s+(\w+-\w+)\s+up\s+up'

    # match = re.search(pattern, data)

    # if match:
    #     slot = match.group(1)
    #     card_type = match.group(2)
    #     print(f"Slot {slot} has {card_type}")
    # else:
    #     print("No match found")


    # match = re.search(r"1\s+(.*?)\s+", data)
    # if match:
    #     slot_1_value = match.group(1)
    #     print("Slot 1 value: ", slot_1_value)

    # # extract the value of 'cpm-2s' from 'Slot A'
    # match = re.search(r"A\s+(.*?)\s+", data)
    # if match:
    #     slot_A_value = match.group(1)
    #     print("Slot A value: ", slot_A_value)