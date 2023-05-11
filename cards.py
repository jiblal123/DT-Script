import paramiko 
import time 

from Nodeconfig import config
class card():
    """This class is because it , it is discovered that the NSP uses different card names than Containerlab. 
    For example, with the exception of R1-PE and R5-PE in Layer 2 Topology , the CP card name is "Card_sfm5_e" in NSP. 
    However, when this card is checked using Secure Shell, it is named "cpm5." Containerlab requires the use of "cpm5" since it understands things differently than NSP.
      Since the correct card name is on the remote server, it is better to extract the card name from the server rather than translating it from the API """
    def __init__(self, ne_id= "10.10.10.5", 
                 hostname= "xxx.xx.xxx.xx6", 
                 username='###', 
                 password='######',
                 logInUsernameForNode= "",
                 loginPasswordForNode= "") -> None:
        self.hostname= hostname #Name of host or IP address of host which will be send node data
        self.userName= username # username for that host
        self.password = password # password for that host
        self.config= config() # Creating Instance of COnfig class in oder to download configuration of nodes.
        self.logInUsernameForNode= logInUsernameForNode
        self.loginPasswordForNode= loginPasswordForNode
               
        pass
    def getcard(self, ne_id, ne_name="something"):
        """This Function established SSH connection to the remote sever to get card details. """

        # id to identify router , so that the configuration file can be rename as ne_name
        indexOfLastZiffer = ne_id.rfind(".")
        nodeName= ne_name
                        
        var= int(ne_id[indexOfLastZiffer+1:]) #getting last digit to map with Nodes name in Remote Server.  
        print("last Ziffer", var) 
        # creating SSH Tunnel and connectiong to the node with PuTTy Credentials
        client = paramiko.SSHClient() 
        #the first time the client connects to a server and the server's host key is not in the known_hosts file,
        #  the client automatically adds the key to the file and proceeds with the connection. 
        # For example By using this function, the client will not prompt the user to confirm whether they want to continue with the connection. 
        # Therefore, the paramiko.AutoAddPolicy() policy prevents the need for the user to type "yes" manually to continue the CLI execution.
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
        client.connect(self.hostname, self.userName, self.password) 
        # With this shell instance the classic CLI command can be executed from Python 
        shell = client.invoke_shell() 
        # sleep is use to simulate human behaviours. Sometime displying data take some time if sleep is not used the full output text may not be displayed
        time.sleep(2) 
        # Classic CLI
        shell.send(f'ssh asad@192.168.100.{30+var}\r\n') # example node Id 10.10.10.1 is mapped as asad@192.168.100.31  and  10.10.10.2 is mapped as asad@192.168.100.32# THis code should not be used in other network because there might be different Login Stucture and differnt credentails. 
        time.sleep(2) 
        shell.send(f'{self.loginPasswordForNode}\r\n') # classic CLI 
        time.sleep(2)
        shell.send('environment no more\r\n') 
        # this command displays the card detail of a node
        shell.send('show card\r\n')# classic CLI 
        time.sleep(2) 
        # this command displays the daughter card detail of a node
        shell.send('show mda\r\n')
        time.sleep(2) # sleep stops program execution to allows tunnel  collect data.  
        
        #collecting all output data
        outputCollection=""
        # loop as long as there is data to receive
        while shell.recv_ready(): 
            tmp = shell.recv(1024) 
        #     # if not tmp: 
        #     #     break 
            #print(tmp.decode())

            outputCollection= outputCollection + tmp.decode() +"\n" # collecting all output from Node. 
            # write the output to a text file
            # this is for the developer convient. No need to write data in file. having data in variable is enough
        with open('output.txt', 'w') as f:
            f.write(outputCollection)
            
        with open('output.txt', 'r') as f:
            data = f.read()
        result = self.get_cp_cP_mda(data)

        # As SSH connection is already established. It is decided to get config data from the same Connection instead of using config API. 
        self.config.getConfigFile(shell, nodeName)

        return result



    def get_cp_cP_mda(self, data):
        """This function extract card detail from the output comming from SSH connection"""
        #spliting data with new lines
        newlines= data.split("\n")
        newlines= [x for x in newlines if x] # removing white space lines
        card1 = ""          #line Card
        mda    = ""         #Daughter Card 
        cp   =""            # cp card Processor Card
       
        word = 'Card Summary'
        #finding word called Card Summary 
        for line in newlines:
            # if word found
            if word in line:
                # index of the word
                index= newlines.index(line)
                #print(f"{word} found in, index {index}")
                # removing unnecessary white space. if the string is like " the      brown      fox    ". This function makes it "hello brown fox"
                cardwithSlot= ' '.join(newlines[index+5].split()) 
                card1= (cardwithSlot.split(" "))[1]
                #Navigating to find CP card and remobing all unnecessary white space
                processorCard= ' '.join(newlines[index+6].split()) # removing unnecessary white space
                cp=             (processorCard.split(" "))[1] # collecting CP card detail
                #print(processorCard)
                
        # finding mda
        # same logic as "Card Summary" applied here like   
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
        return {"lc":card1, "cp": cp, "mda":mda  }
    



if __name__ == "__main__":
    obj = card()
    result= obj.getcard("10.10.10.8")
    print("card:", result["lc"], "cp", result["cp"], "mda", result["mda"])    



       




    
    """some try and error code to find card name"""
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