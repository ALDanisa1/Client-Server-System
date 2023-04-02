#Anele Danisa
#DNSANE001
#Client implementation

from socket import *
import os
import hashlib
from os.path import *
import math
import sys


# Method to upload a file to a server
def upload_file():
    print(client_socket.recv(1024).decode())
    filename=input(" ->>>> ")
    fileSize = os.stat(filename).st_size
    client_socket.sendall(filename.encode())
    print(client_socket.recv(1024).decode())
    status = input(" ->>>> ")
    
    #create a header and send it to server
    header = hostname + "#"+ status + "%"+ str(fileSize)
    
    

    client_socket.sendall(header.encode())
    print(client_socket.recv(1024).decode())
     
    file=open(filename,"rb") # Opening file to be sent 
    file_content=file.read(1024)
    i = 1
    packets = math.ceil(fileSize/1024)
    while i < packets+1:
        client_socket.sendall(file_content)
        file_content=file.read(1024)
        while len(file_content) < 1024:
            file_content = file_content + bytes(" ".encode())
        
        i = i + 1
        
    #client_socket.send("finished".encode())
    print("The file was successfully sent to the server")
    client_socket.send(generate_hashvalue(filename).encode())
    print("The Hash value was successfully sent to a server")
   
    
    file.close()    
    print(client_socket.recv(1024).decode())
    print(client_socket.recv(4096).decode())
    
# Method to receive file from server
def download_file():
    
    print("List of Available files: ")
    message = client_socket.recv(1024).decode()
    
    if message == "No files available":
        print(message)
        return
    else:
        print(message)
    
    print("choose the file name you want to upload")
    filename=input(" ->>>> ")
    client_socket.send(filename.encode())
    
    fileExist = client_socket.recv(1024).decode()
    
    if fileExist != "A":
        print("no file")
        return
    
    # Client receiving file bytes from server
    contents=bytes("".encode())
    
    filesize = client_socket.recv(1024).decode()
    filesize = int(filesize)
    
    bLoad = 0
    while bLoad < filesize:
        file_content=client_socket.recv(1024)
        contents=contents + file_content
        bLoad = bLoad + 1024
    
    contents = contents[:filesize] 
    
    print("Opening file received from a server")
    file=open(filename,"wb")  #opening file 
    print("Writing all the file content inside a file.......")
    file.write(contents) #writing file to a client dir
    print("The File was successfully downloaded,it now available for use on your directory!!")

# Calculating hash value
def generate_hashvalue(filename):
    # Using working directory 
    wdir=path+"\\"
    wdir+=filename
    # Getting hash value of file
    hashval=hashlib.sha1()
    section=0
    with open(filename,"rb") as file:
        section=0
        while section!=b'':
            section=file.read(1024)
            hashval.update(section)
    # Return final hash value
    return hashval.hexdigest()

def DeleteFile():
    print(client_socket.recv(1024).decode())
    filename=input(" ->>>> ")
    client_socket.send(filename.encode())

def LoadList():
    print(client_socket.recv(1024).decode())  
    
    
def main() :
    # Communication with server:
    menu = client_socket.recv(1024).decode()
    print(menu) 
    message=input(" ->>>> ")
    # "3" is the terminating message
    while message!="5":
        client_socket.send(message.encode())
        if message=="1":
            upload_file()
        elif message=="2":            
            download_file()
        elif message=="3":            
            DeleteFile()
        elif message=="4":            
            LoadList()
        feedback=client_socket.recv(1024).decode()
    
        print(feedback)
        message=input(" ->>>>")
    client_socket.send(message.encode())
    client_socket.close()



if __name__ == "__main__":
    if len(sys.argv) != 3:
        #default values
        #hostname = "client_2" 
        #port=5000
        print("d")
    else:
        hostname = sys.argv[1]
        port = sys.argv[2]  
    
    
    # Creating file that contains all saved files should it not exist yet
    file_avail=open("availfiles.txt","a")
    file_avail.close()
    # Establishing client
    port=5000
    client_socket=socket(AF_INET,SOCK_STREAM)
    client_socket.connect((gethostname(),port))
        
    #create the hostname link
    hostname = "client_2" 
    #get the current path
    path = os.path.dirname(os.path.abspath(__file__))
        
    client_socket.sendall(hostname.encode())
    main()