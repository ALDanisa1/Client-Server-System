# Server implementation
# This program seeks to transfer files from client

# Importing all necessary libraries
import os
from socket import *
import hashlib
from os.path import *
import threading
import math

# Declaring string of menu
menu="Please select one of the following services:\n1: Upload a file\n2: Download a file\n3: Delete a file\n4: List files\n5: Terminate connection"

clienthost=""

# array which will store available files to user
avail_files=[]
# Establishing server
host="servername"
port=5000
server_socket=socket(AF_INET,SOCK_STREAM)
server_socket.bind((gethostname(),port))
server_socket.listen(5)

file_avail=open("availfiles.txt","a+") #Create file it doesn't already exist
file_avail.close()

print("SERVER NOW RUNNING")

# Method which will instantiate avail_files array
def avail_file(header):
    file=open("availfiles.txt","r")
    allfiles=file.readlines()
    # Looping through all files in array
    for i in range(0,len(allfiles),2):
        # Getting header from all files
        header=allfiles[i+1]
        # Splitting the header into parts
        hostname=header[0:header.index("#")]
        privacy=header[header.index("#")+1]
        # Only allowing user to access accessible files, also don't add the file if its already present
        if (hostname==clienthost or privacy==1) and allfiles[i][0:allfiles[i].index("\n")] not in avail_files:
            avail_files.append(allfiles[i][0:allfiles[i].index("\n")])

# Method which returns path where file is saved:
def get_path():
    return(os.path.dirname(os.path.abspath(__file__)))

# Method which will hash file for comparison 
def hash_file(filename):
    dir=get_path()+"\\"+filename
    hashval=hashlib.sha1()
    section=0
    with open(dir,"rb") as file:
        section=0
        while section!=b'':
            section=file.read(1024)
            hashval.update(section)
    return hashval.hexdigest()

# Method which will transfer files
def recv_file(filename,contents,hash,header,connection):
    # Opening file to be written to
    file=open(get_path()+"\\"+filename,"wb")
    # Writing contents of client file to new file
    print("Writing contents")
    file.write(contents)
    # Check the hash value of the file
    hashval=hash_file(filename)
    # Comparing two hash values:
    if hashval==hash:
        pass
    else:
        print("Missing bytes!")
    # Closing file
    file.close()
    # Adding the file name to available files
    if(file_format(filename,header) not in avail_files):
        avail_files.append(file_format(filename,header))
        save(filename,header)
        connection.sendall("Saved".encode())
    else:
        connection.sendall("File already exists!".encode())

# Method to create specified format for availfiles.txt and availfiles list
def file_format(filename,header):
    # Using # as delimiter because host names cannot contain this character
    return filename+"\n"+header

# Method to receive file contents from connection:
def getfile(connection):
    connection.sendall("Please give the name of the file you wish to upload".encode())
    filename=connection.recv(1024).decode()
    # Requesting privacy permissions from the user
    connection.sendall("1: Open\n2:Protected".encode())
    # Receiving header from user:
    header=connection.recv(1024).decode()
    fileSize = int(header[header.index("%") + 1:])

    if fileSize == 0:
        return
    # Ensuring all contents are recovered:
    connection.sendall(f"Uploading file {filename}...".encode())
    contents=bytes("".encode())
    # Ensuring that all bytes make it through the buffer
    bytesLoaded = 0

    while bytesLoaded < fileSize:
        segment=connection.recv(1024)
        contents+=segment #Append packet to total file contents
        bytesLoaded += 1024

    print("File recieved")

    contents = contents[:fileSize] #Make contents only contain bytes from file

  # Getting the hash value of the file from user perspective 
    hashval=connection.recv(1024).decode()
    # Putting file onto server
    recv_file(filename,contents,hashval,header,connection)

def create_file_list(connection):
    temp="" 
    for i in range(len(avail_files)): #Loop through availfiles list
        temp = temp + avail_files[i] + "\n" #Add files to string

    if temp == "" : #If no files
        connection.sendall("No files available".encode()) #Notify the client
        return False #Exit out function
    else:
        connection.sendall(temp.encode()) #Send list of files

    return True


# Method to allow user to download a file from the server
def download_file(connection):
    if create_file_list(connection) == False :
        return

    filename=connection.recv(1024).decode()
    print(filename)
    # File will only be opened if available to user (open/protected for specific user)
    if str(filename) in str(avail_files):
        connection.sendall("A".encode()) #File does exist, notify client
        # Open file for reading only (bytes)
        print("Client downloading file...")
        file=open(get_path()+"\\"+filename,"rb")
        fileSize = os.stat(filename).st_size
        connection.sendall(str(fileSize).encode())
        # Get all contents from the file
        segment=file.read(1024)

        numOfPackets = math.ceil(fileSize/1024)
        i = 1
        while i < numOfPackets + 1:
            connection.sendall(segment)
            segment=file.read(1024)
            while len(segment) < 1024: #If packet size is less than 1024 bytes
                segment = segment + bytes(" ".encode()) #Add characters to end to keep consistant packet size
        
            i = i + 1

        file.close()
        print("File successfully downloaded by client")
    else:
        connection.sendall("N/A".encode()) #File does not exist, notify client

# Method to append uploaded files to text file
def save(filename,header):
    file=open("availfiles.txt","a")
    file.write(filename+"\n")
    file.write(header+"\n")
    file.close()

def delete_file(connection):
    connection.send("Please give the name of the file you wish to delete".encode())
    filename=connection.recv(1024).decode()    
    if str(filename) in str(avail_files) :
        connection.sendall("File was successfully deleted".encode('ascii'))
        os.remove(filename)
        for i in avail_files: #Iterate through the available files list
            if str(filename) in str(i):
                avail_files.remove(i) #And delete the required one
    else :
        connection.sendall("File does not exist or you lack required permissions".encode('ascii'))


def threader():
# Loop to attain connections and to 
    while True:
        # Instantiating avail_files array
        avail_file(clienthost)
        print("Current client host name:",clienthost)
        # Giving user necessary options
        connection.sendall(menu.encode())
        # Getting message from client
        message=connection.recv(1024).decode()
        print(message)
        # "1" means that the user would like to upload a file
        if message=="1":
            # Created methods to upload file
            print("Client requesting to upload file")
            getfile(connection)
        # "2" means that the user would like to download a file
        elif message=="2":
            print("Client requesting to download file")
            download_file(connection)
        # "3" means that the user would like to delete a file
        elif message=="3":
            print("Client requesting to delete file")
            delete_file(connection)
        elif message=="4":
            print("Client wants to list files")
            create_file_list(connection)
        # "5" means that the user would like to terminate the connection
        elif message=="5":
            print("Client terminating connection")
            connection.close()
            break
        # handling invalid input, user will be prompted to reenter info
        else:
            connection.sendall("Invalid input\n".encode())

# Code which will wait for incoming connections
while True:
    connection,addr=server_socket.accept()
    print(f"Established connection from {addr}")
    clienthost=connection.recv(1024).decode()
    print(f"Name of current host {clienthost}")
    # Starting thread
    client_thread=threading.Thread(target=threader)
    client_thread.start()