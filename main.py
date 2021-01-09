import requests

#Function for sending request for 'cp' command
def cp_function(param1, param2):
        serverURL = "http://localhost:3000/cp"
        dataSet = {'file1': param1,
                   'file2': param2
                   }
        #Sending post request and saving response as response object
        r = requests.post(url=serverURL, data=dataSet)
        #Extracting response text
        responseRequest = r.text
        print("Response request: %s" % responseRequest)


#Function for sending request for 'mv' command
def mv_function(param1,param2):
        serverURL = "http://localhost:3000/mv"
        dataSet = {'oldPath': param1,
                   'newPath': param2
                   }
        r = requests.post(url=serverURL, data=dataSet)
        responseRequest = r.text
        print("Response request: %s" % responseRequest)


#Function for sending request for 'mkdir' command
def mkdir_function(param):
        serverURL = "http://localhost:3000/mkdir"
        dataSet = {'pathDir': param}
        r = requests.post(url=serverURL, data=dataSet)
        responseRequest = r.text
        print("Response request: %s" % responseRequest)

# Function for sending request for 'rm' command
def rm_function(param):
        serverURL = "http://localhost:3000/rm"
        dataSet = {'pathRm': param}
        r = requests.post(url=serverURL, data=dataSet)
        responseRequest = r.text
        print("Response request: %s" % responseRequest)

# Function to upload one file from local directory to remote directory
def put_function(param1, param2):
        with open(param1, "rb") as a_file:
                list = param1.split('/')
                file_name = list[len(list)-1]
                file_dict = {file_name: a_file}
                response = requests.post("http://localhost:3000/put", files=file_dict, data={"path": param2})
                print("Response request: %s" % response.text)

# Function to get one file from remote directory to local directory
def get_function(param1, param2):
        response = requests.get(url='http://localhost:3000/get', data={"path": param1})
        with open(param2, "wb") as f:
                f.write(response.content)


# Function to return all available commands
def list_commands():
        listCommands = {
                'cp': 'The cp command contains two file names, then it copy the contents of 1st file to the 2nd file.',
                'mv': 'The mv command moves files from one place to another.',
                'mkdir': 'The mkdir (make directory) command is used to make a new directory.',
                'rm': 'The rm command removes file specified.',
                'put': 'The put command is used to upload one file from local directory to remote directory.',
                'get': 'The put command is used to get one file from remote directory local directory.'
        }
        return listCommands

# Function to provide information about available commands and the shell environment
def print_help():
        print("Instruction:")
        print('Use \"dbxcli\" followed by the command and the space-separated parameters.')
        print("Use \"help\" command to provide information about available commands and the shell environment.")
        print("Use \"exit\" command to stop the program.\n")
        print('Available commands:')
        listCommands= list_commands()
        for command in listCommands.keys():
                print("Command %s : %s" %(command,listCommands[command]))


def check_invalid_command(command):
        commandParts = command.split()
        if (len(commandParts) < 2 or len(commandParts)>4):
                return False
        if (commandParts[0] != 'dbxcli'):
                return False
        com = commandParts[1]
        if(com != 'exit' and com !='help' and len(commandParts) == 2):
                return False
        if ((com == 'exit' or com == 'help') and len(commandParts) != 2):
                return False
        listCommands = list_commands().keys()
        if((com not in listCommands) and com != 'exit' and com !='help'):
                return False
        if(com in ['cp','mv','put','get'] and len(commandParts)!=4):
                return False
        if(com in ['mkdir','rm'] and len(commandParts)!=3):
                return False
        return True




def getUserCommand():
        print_help()
        while(1):
                command = input("Command: ")
                while (check_invalid_command(command)==False):
                       command = input("Incorrect/Invalid command. Try again: ")
                com = command.split()[1]
                param1= command.split()[2] if len(command.split())>=3 else None
                param2= command.split()[3] if len(command.split())==4 else None
                if(com=='cp'):
                        cp_function(param1, param2)
                if(com=='mv'):
                        mv_function(param1,param2)
                if (com == 'put'):
                        put_function(param1,param2)
                if (com == 'get'):
                        get_function(param1, param2)
                if(com=='mkdir'):
                        mkdir_function(param1)
                if(com=='rm'):
                        rm_function(param1)
                if (com == 'exit'):
                        print("Exit program")
                        break
                if (com == 'help'):
                        print_help()


getUserCommand()
