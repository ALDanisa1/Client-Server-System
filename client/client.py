
import hashlib
import socket
import imghdr

# create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()
client_no = "client_1"


port = 9999

# connect the client socket to the server
client_socket.connect((host, port))
#sending a message to the server
print ("\n******************Welcome to the server***************\n")
print ("Please choose from the options below \n")
print("1 = upload a file \n")
print("2 = download a file \n")
print("3 = check available files \n") 
print("4 = Delete file from a server \n")
print("5 = Disconnect from server \n")

client_socket.sendall(client_no.encode())
option = input()
client_socket.sendall(option.encode())

while option != '5' :    
    # send file name to server
    if option == "1":
        filename = input("Enter the name of the file you want to upload\n")
        client_socket.sendall(filename.encode('ascii'))
        
        # read file content and send to server  
        
        with open(filename, "r") as f:
            filecontent = f.read().encode()
        
        client_socket.sendall(filecontent)
        
        check = hashlib.sha224(filecontent).hexdigest()
        client_socket.sendall(check.encode())
       
        # receive confirmation message from server
        status1 = input("Enter the status of this file (open) or (protected) \n")
        client_socket.sendall(status1.encode()) 
        
        print(client_socket.recv(1024).decode('ascii'))
        
   
        
    elif option  == "2":
        filename = input("Enter the name of the file you want to download\n")
        client_socket.sendall(filename.encode('ascii'))
        
        # receive file content from server
        filecontent = client_socket.recv(1024).decode('ascii')
        
        if filecontent == "Not found" :
            print("The file you are looking for does not exist or it protected")
        elif filecontent =="Not Valid" :
            print("The file you are looking for is corrupted")
        else:
            # save file to disk
            with open("downloded.txt", "w") as f:
                f.write(filecontent)
    elif option == "3" :
        print(client_socket.recv(1024).decode('ascii'))
        status = input()
        client_socket.sendall(status.encode('ascii'))
        print(client_socket.recv(1024).decode('ascii'))
        
    elif option == "4" :
        print(client_socket.recv(1024).decode('ascii'))
        filename = input()
        client_socket.sendall(filename.encode('ascii'))
        print(client_socket.recv(1024).decode('ascii'))       
    elif option == "5" :
        filename = input("Enter the name of the file you want to update\n")
        client_socket.sendall(filename.encode('ascii'))
    
    print ("\nPlease choose from the options below \n")
    print("1 = upload a file \n")
    print("2 = download a file \n")
    print("3 = check available files \n") 
    print("4 = Delete file from a server \n")
    print("5 = Disconnect from server \n")
    option = input()
    client_socket.sendall(option.encode())


#close the client socket
client_socket.close()




