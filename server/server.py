import socket
import array
import threading
import hashlib
import os


# create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# get local machine name
host = socket.gethostname()

port = 9999

#creating list of files to be uploaded
Files = []
client_files = {}
check_files = {}
client_no = 0

# bind the socket to a public host, and a well-known port
server_socket.bind((host, port))

# become a server socket
server_socket.listen(3)

print("Server started. Waiting for connections...")

def Update_Database(filename, status1, client_no):   
    if status1 == 'open':
        Files.append(filename)
    elif status1 == 'protected':
        if client_no not in client_files:
            client_files[client_no] = []
        client_files[client_no].append(filename)
    
    print(client_files)
    print(Files)


def upload():

    # receive file name from client
    filename = client_socket.recv(1024).decode('ascii')
   
    # receive file content from client
    filecontent = client_socket.recv(1024).decode('ascii')
    check = client_socket.recv(1024).decode()

    if filename not in check_files:
        check_files[filename] = "" 
    check_files[filename] = check
  
    # save file to disk
    with open(filename, "w") as f:
        f.write(filecontent)   
    #receive the message
    status1= client_socket.recv(1024).decode('ascii')
    #update the database
    Update_Database(filename, status1, client_no)
    # send confirmation message to client
    client_socket.sendall("File uploaded successfully!".encode('ascii'))
    print(client_no, "uploaded a file")
    
    

def download():
     # receive file name from client
    filename = client_socket.recv(1024).decode('ascii')
    #check if the client has acces over file
    if filename in Files or (client_no in client_files and filename in client_files[client_no] ) :
        #client_socket.sendall(filename.encode('ascii'))
        # read file content and send to server 
        with open(filename, "r") as f:
            filecontent = f.read().encode()            
        check = hashlib.sha224(filecontent).hexdigest()
        if filename in check_files :
            #check for validation
            if check == check_files[filename]:
                client_socket.sendall(filecontent)
            else:
                client_socket.sendall("Not Valid".encode('ascii'))                 
          
        else :
            response2 = "Not found"
            client_socket.sendall(response2.encode('ascii'))  
            
            
    else:
        response2 = "Not found"
        client_socket.sendall(response2.encode('ascii')) 
        
        
#takes in the status of list the client is lokking for and send the list of files to the client if the list is not empty         
def getList(status):
    result = ""
    if status == 'open' and len(Files) > 0:
        for i in Files :
            result += i +'\n'
        client_socket.sendall(result.encode('ascii'))
    elif status == 'protected' and len(client_files) > 0 :
        for i in client_files[client_no] :
            result += i +'\n'
        if result == "" :
            client_socket.sendall("you haven't uploaded any files".encode('ascii'))
        client_socket.sendall(result.encode('ascii'))
    else :
        client_socket.sendall("The list you looking for is empty".encode('ascii'))

def DeleteFile(filename):
    os.remove(filename)
    if filename in Files :
        Files.remove(filename)
    elif filename in client_files[client_no] :
        client_files[client].remove(filename)
    else :
        client_socket.sendall("you have no acces over the file you want to delete".encode('ascii'))

    client_socket.sendall("File was successfully Deleted".encode('ascii'))

    
def client_Handler() :
    while True:
        option = client_socket.recv(1024).decode()
        if not option:
            break    
        if option == "1":
            upload()
                
        elif option == "2" :
            download()
            
        elif option == "3" :
            client_socket.sendall("You want a list of your protected files or open files? type open or protected".encode('ascii'))
            List_type =  client_socket.recv(1024).decode('ascii')
            getList(List_type) 
        elif option == "4" :
            client_socket.sendall("Enter the nname of a file you want to delete".encode('ascii'))
            filename =  client_socket.recv(1024).decode('ascii')
            DeleteFile(filename)
        
        # close connection with client               
    client_socket.close()
    print("Connection closed by client ", addr )   
        
# continuously listen for incoming connections
while True:
    # accept connection from a client
    client_socket, addr = server_socket.accept()
    print("Got the connection from ", addr)

    client_no = client_socket.recv(1024).decode()    
    # create a new thread to handle the client connection
    client_thread = threading.Thread(target=client_Handler)
    client_thread.start()        
        
# close the server socket
server_socket.close()
exit()