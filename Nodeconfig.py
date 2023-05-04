
import paramiko 
import time 

class config():
    def __init__(self ) -> None:
        print("I am from config")
        # self.ne_id= ne_id
        # result= self.getcard(self.ne_id)
        # print(result)
        # self.cardDetail={}
        pass


    def getConfigFile(self, shell, ne_name= "r1"):






        # # get configuration from SSH tunnel. 
        # client = paramiko.SSHClient() 
        # client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
        # client.connect('147.75.202.26', username='root', password='Changeme1!') 
        # shell = client.invoke_shell() 
        # time.sleep(2) 
        # shell.send(f'ssh asad@192.168.100.31\r\n') # CLASSIC CLI 
        # time.sleep(2) 
        # shell.send('NokiaNsp!\r\n') # MD CLI 
        # time.sleep(2) 
        shell.send('environment no more\r\n')
        time.sleep(2) 
        shell.send('admin display-config\r\n')
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

            outputCollection= outputCollection + tmp.decode() #+"\n" # collecting all output from Node.

            # write the output to a text file

        #print((outputCollection))
        StartingIndex= outputCollection.find("# TiMOS")
        EndingIndex= outputCollection.rfind("# Finished")
        print(StartingIndex, "---------",EndingIndex)
        print(outputCollection[EndingIndex])

        print (outputCollection[StartingIndex:EndingIndex])
        #print(outputCollection)

        with open(f'configData/{ne_name}config.txt', 'w') as f:
                f.write(outputCollection[StartingIndex:EndingIndex])
        shell.close()