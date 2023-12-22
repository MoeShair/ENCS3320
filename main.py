from socket import *

#Initializing the port and the socket
serverPort = 9966
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(("",serverPort))
serverSocket.listen(1)


print ("The server is ready to receive")
while True: #Infinite loop, waits for the user to access a webpage
    try:
        connectionSocket, addr= serverSocket.accept() #accepting the request
        sentence = connectionSocket.recv(2048).decode() #Decoding it and putting the request in sentence
        #printing the address and the HTTP request
        print (addr)
        print (sentence)
        ip = addr[0] #Getting the IP address and the port of the client
        port = addr[1]
        #Splitting the lines to get the path
        requestLines = sentence.split("\r\n")
        requestParts = requestLines[0].split(" ")
        path = requestParts[1]  # path
        if path =="/": #if statement for if the path is "/", setting its new value to index.html
            path = "/index.html"
        if path == "/main_ar.html" or path == "/ar" : #if statement for the arabic webpage
            connectionSocket.send("HTTP/1.1 200 OK \r\n".encode()) #Sending the ok, meaning that the connection was successful
            connectionSocket.send("Content-Type: text/html; charset=utf-8\r\n".encode()) #setting th type to an HTML file
            connectionSocket.send("\r\n".encode()) #adding \r\n to end the HTTP request and encoding it
            #Applying the file and sending the data
            f1 = open("main_ar.html", "rb")
            data=f1.read()
            connectionSocket.send(data)

            #Same thing for arabic webpage, except it covers all cases mentioned in the project for EN webpage
        elif path=="/index.html" or path=="/en" or path == "/main_en.html" or path=="/" or path.endswith(".html"):
            connectionSocket.send("HTTP/1.1 200 OK \r\n".encode())
            connectionSocket.send("Content-Type: text/html; charset=utf-8\r\n".encode())
            connectionSocket.send("\r\n".encode())
            f1 = open("main_en.html", "rb")
            data=f1.read()
            connectionSocket.send(data)

            #CSS Handling
        elif path  == "/styles.css" or path.endswith(".css"):
            connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
            connectionSocket.send("Content-Type: text/css\r\n".encode()) #Setting the type to CSS this time
            connectionSocket.send("\r\n".encode())
            with open("styles.css", "rb") as css_file:
                css_data = css_file.read()
            connectionSocket.send(css_data)

            #Same thing applies for all images, except we set the type to png or jpg depending on the image extension
        elif path == "/img/Network.png" or path.endswith(".png"):
            connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
            connectionSocket.send("Content-Type: image/png\r\n".encode())
            connectionSocket.send("\r\n".encode())
            with open("img/pngpicture.png", "rb") as img_file:
                img_data = img_file.read()
            connectionSocket.send(img_data)

        elif path == "/img/Networks2.jpg" or path.endswith(".jpg"):
            connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
            connectionSocket.send("Content-Type: image/jpeg\r\n".encode())
            connectionSocket.send("\r\n".encode())
            with open("img/Network1.jpg", "rb") as img_file:
                img_data = img_file.read()
            connectionSocket.send(img_data)

        elif path == "/img/Networks3.jpg":
            connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
            connectionSocket.send("Content-Type: image/jpeg\r\n".encode())
            connectionSocket.send("\r\n".encode())
            with open("img/Networks3.jpg", "rb") as img_file:
                img_data = img_file.read()
            connectionSocket.send(img_data)
            
        elif "GET /cr" in sentence: #Redirecting to cornell
            connectionSocket.send("HTTP/1.1 307 Temporary Redirect\r\n".encode()) #Sending the 307 meaning temporary redirection
            connectionSocket.send(f"Location: http://cornell.edu\r\n".encode()) #Setting location
            connectionSocket.send("\r\n".encode()) #Ending request

        elif "GET /so" in sentence:
            #Same thing as above, but for stack overflow
            connectionSocket.send("HTTP/1.1 307 Temporary Redirect\r\n".encode())
            connectionSocket.send(f"Location: http://www.stackoverflow.com\r\n".encode())
            connectionSocket.send("\r\n".encode())

        elif "GET /rt" in sentence:
            #Same thing as above, but for Rita website 
            connectionSocket.send("HTTP/1.1 307 Temporary Redirect\r\n".encode())
            connectionSocket.send(f"Location: https://ritaj.birzeit.edu\r\n".encode())
            connectionSocket.send("\r\n".encode())

        else:
            #Else statement to cover the error case, when the user makes a spelling mistake or the file doesn't exist
            connectionSocket.send("HTTP/1.1 404 Not Found \r\n".encode()) #Sending the appropriate code (404 not found)
            connectionSocket.send("Content-Type: text/html; charset=utf-8\r\n".encode())
            connectionSocket.send("\r\n".encode())

            #Reading the Error.html file, then putting the IP and port initialized in the beginning 
            with open("Error.html", "rb") as f1:
                data = f1.read().decode('utf-8')

            data = data.replace("ip", ip)
            data = data.replace("port", str(port))

            connectionSocket.send(data.encode('utf-8')) 
        connectionSocket.close()
    except:
        print ("IO error")
    else:
        print ("OK")